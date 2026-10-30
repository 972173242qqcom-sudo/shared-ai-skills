import Foundation
import AVFoundation
import Vision
import CoreImage
import CoreVideo

enum ProcessorError: Error, CustomStringConvertible {
    case usage
    case noVideoTrack
    case cannotAddReaderOutput
    case cannotAddWriterInput
    case cannotStartReader(String)
    case cannotStartWriter(String)
    case missingPixelBuffer
    case cannotCreateAnalysisImage(Int)
    case noForeground(Int)
    case cannotAllocateOutputBuffer
    case appendFailed(String)
    case readerFailed(String)
    case writerFailed(String)

    var description: String {
        switch self {
        case .usage: return "Usage: make_transparent <input.mp4> <output.mov>"
        case .noVideoTrack: return "Input has no video track"
        case .cannotAddReaderOutput: return "Cannot add AVAssetReader output"
        case .cannotAddWriterInput: return "Cannot add AVAssetWriter input"
        case .cannotStartReader(let message): return "Cannot start reader: \(message)"
        case .cannotStartWriter(let message): return "Cannot start writer: \(message)"
        case .missingPixelBuffer: return "Decoded sample has no image buffer"
        case .cannotCreateAnalysisImage(let frame): return "Cannot create Vision analysis image at frame \(frame)"
        case .noForeground(let frame): return "Vision found no foreground at frame \(frame)"
        case .cannotAllocateOutputBuffer: return "Cannot allocate output pixel buffer"
        case .appendFailed(let message): return "Failed to append frame: \(message)"
        case .readerFailed(let message): return "Reader failed: \(message)"
        case .writerFailed(let message): return "Writer failed: \(message)"
        }
    }
}

func waitForWriter(_ input: AVAssetWriterInput, writer: AVAssetWriter) throws {
    while !input.isReadyForMoreMediaData {
        if writer.status == .failed || writer.status == .cancelled {
            throw ProcessorError.writerFailed(writer.error?.localizedDescription ?? "unknown error")
        }
        usleep(2_000)
    }
}

func removeBackgroundMatte(
    source: CVPixelBuffer,
    destination: CVPixelBuffer,
    preservePremultipliedEdgeRGB: Bool
) {
    CVPixelBufferLockBaseAddress(source, .readOnly)
    CVPixelBufferLockBaseAddress(destination, [])
    defer {
        CVPixelBufferUnlockBaseAddress(destination, [])
        CVPixelBufferUnlockBaseAddress(source, .readOnly)
    }

    guard let sourceBase = CVPixelBufferGetBaseAddress(source),
          let destinationBase = CVPixelBufferGetBaseAddress(destination) else { return }
    let width = min(CVPixelBufferGetWidth(source), CVPixelBufferGetWidth(destination))
    let height = min(CVPixelBufferGetHeight(source), CVPixelBufferGetHeight(destination))
    let sourceRowBytes = CVPixelBufferGetBytesPerRow(source)
    let destinationRowBytes = CVPixelBufferGetBytesPerRow(destination)
    let sourceBytes = sourceBase.assumingMemoryBound(to: UInt8.self)
    let destinationBytes = destinationBase.assumingMemoryBound(to: UInt8.self)

    // This product footage changes from a white background to a black one.
    // Detect the current matte from the four corners before repairing edge RGB.
    let insetX = min(max(0, width / 100), max(0, width - 1))
    let insetY = min(max(0, height / 100), max(0, height - 1))
    let samplePoints = [
        (insetX, insetY),
        (max(0, width - 1 - insetX), insetY),
        (insetX, max(0, height - 1 - insetY)),
        (max(0, width - 1 - insetX), max(0, height - 1 - insetY))
    ]
    var backgroundLevel = 0
    for (x, y) in samplePoints {
        let pixel = sourceBytes.advanced(by: y * sourceRowBytes + x * 4)
        backgroundLevel += (Int(pixel[0]) + Int(pixel[1]) + Int(pixel[2])) / 3
    }
    let backgroundIsLight = backgroundLevel / samplePoints.count >= 128

    for y in 0..<height {
        let sourceRow = sourceBytes.advanced(by: y * sourceRowBytes)
        let destinationRow = destinationBytes.advanced(by: y * destinationRowBytes)
        for x in 0..<width {
            let offset = x * 4
            let alpha = Int(destinationRow[offset + 3])
            let whiteContribution = 255 - alpha
            if alpha == 0 {
                destinationRow[offset + 0] = 0
                destinationRow[offset + 1] = 0
                destinationRow[offset + 2] = 0
            } else if alpha < 255 {
                if backgroundIsLight && !preservePremultipliedEdgeRGB {
                    // White matte: observed = foregroundPremultiplied + white * (1 - alpha).
                    destinationRow[offset + 0] = UInt8(max(0, Int(sourceRow[offset + 0]) - whiteContribution))
                    destinationRow[offset + 1] = UInt8(max(0, Int(sourceRow[offset + 1]) - whiteContribution))
                    destinationRow[offset + 2] = UInt8(max(0, Int(sourceRow[offset + 2]) - whiteContribution))
                }
                // With an intentionally inset mask, the new feather lies inside clean product
                // pixels rather than on the original source/background antialias. In that mode,
                // keep Core Image's premultiplied RGB on every frame so white- and black-matte
                // sections use one consistent edge-color rule.
            }
        }
    }
}

func repairStylusBodyAlpha(source: CVPixelBuffer, destination: CVPixelBuffer) {
    CVPixelBufferLockBaseAddress(source, .readOnly)
    CVPixelBufferLockBaseAddress(destination, [])
    defer {
        CVPixelBufferUnlockBaseAddress(destination, [])
        CVPixelBufferUnlockBaseAddress(source, .readOnly)
    }
    guard let sourceBase = CVPixelBufferGetBaseAddress(source),
          let destinationBase = CVPixelBufferGetBaseAddress(destination) else { return }

    let width = min(CVPixelBufferGetWidth(source), CVPixelBufferGetWidth(destination))
    let height = min(CVPixelBufferGetHeight(source), CVPixelBufferGetHeight(destination))
    let sourceRowBytes = CVPixelBufferGetBytesPerRow(source)
    let destinationRowBytes = CVPixelBufferGetBytesPerRow(destination)
    let sourceBytes = sourceBase.assumingMemoryBound(to: UInt8.self)
    let destinationBytes = destinationBase.assumingMemoryBound(to: UInt8.self)
    let yStart = Int(Double(height) * 0.45)
    let fitEnd = Int(Double(height) * 0.86)
    let xLimit = Int(Double(width) * 0.44)
    let interiorStart = Int(Double(width) * 0.39)
    let interiorWidth = max(1, xLimit - interiorStart)
    var boundaries = [Int](repeating: -1, count: height)
    var fillEnds = [Int](repeating: -1, count: height)

    // Work on the actual rendered Alpha plane. This avoids color-channel and
    // coordinate ambiguity when round-tripping Vision's one-component mask.
    for y in yStart..<height {
        let row = destinationBytes.advanced(by: y * destinationRowBytes)
        var interiorForeground = 0
        for x in interiorStart..<xLimit where row[x * 4 + 3] >= 128 {
            interiorForeground += 1
        }
        guard interiorForeground * 100 >= interiorWidth * 60 else { continue }
        for x in 0..<xLimit where row[x * 4 + 3] >= 128 {
            boundaries[y] = x
            break
        }
        for x in stride(from: xLimit - 1, through: 0, by: -1) where row[x * 4 + 3] >= 128 {
            fillEnds[y] = x + 1
            break
        }
    }

    var count = 0.0
    var sumY = 0.0
    var sumX = 0.0
    var sumYY = 0.0
    var sumYX = 0.0
    if yStart < fitEnd {
        for y in yStart..<fitEnd where boundaries[y] >= 0 {
            let yd = Double(y)
            let xd = Double(boundaries[y])
            count += 1
            sumY += yd
            sumX += xd
            sumYY += yd * yd
            sumYX += yd * xd
        }
    }
    let denominator = count * sumYY - sumY * sumY
    let slope = denominator == 0 ? 0 : (count * sumYX - sumY * sumX) / denominator
    let intercept = count == 0 ? 0 : (sumX - slope * sumY) / count

    for y in yStart..<height where boundaries[y] >= 0 {
        let sourceRow = sourceBytes.advanced(by: y * sourceRowBytes)
        let destinationRow = destinationBytes.advanced(by: y * destinationRowBytes)
        var productStart = boundaries[y]
        var imposeFittedEdge = false
        if count > 20 {
            let bottomWeight = Double(y - yStart) / Double(max(1, height - yStart - 1))
            let edgeInset = Int((2.0 + 6.0 * bottomWeight).rounded())
            productStart = max(
                0,
                min(xLimit - 1, Int((slope * Double(y) + intercept).rounded()) + edgeInset)
            )
            imposeFittedEdge = true

            // Remove outward foreground spikes as well as filling inward bites.
            // The previous pass only added missing Alpha, so small white bumps
            // outside the fitted product silhouette could survive.
            if productStart > 0 {
                for x in 0..<productStart {
                    let offset = x * 4
                    destinationRow[offset + 0] = 0
                    destinationRow[offset + 1] = 0
                    destinationRow[offset + 2] = 0
                    destinationRow[offset + 3] = 0
                }
            }
        }

        // Never extend the repair to a fixed x coordinate. When the stylus is
        // smaller, doing so exposes a rectangular patch past its actual right
        // edge. Preserve the row's detected right boundary instead.
        let fillEnd = max(productStart + 2, min(xLimit, fillEnds[y] >= 0 ? fillEnds[y] : xLimit))
        let fillStart = min(fillEnd, productStart + 2)
        for x in fillStart..<fillEnd {
            let offset = x * 4
            destinationRow[offset + 0] = sourceRow[offset + 0]
            destinationRow[offset + 1] = sourceRow[offset + 1]
            destinationRow[offset + 2] = sourceRow[offset + 2]
            destinationRow[offset + 3] = 255
        }
        if imposeFittedEdge {
            let first = productStart * 4
            destinationRow[first + 0] = sourceRow[first + 0]
            destinationRow[first + 1] = sourceRow[first + 1]
            destinationRow[first + 2] = sourceRow[first + 2]
            destinationRow[first + 3] = 96
            if productStart + 1 < fillEnd {
                let second = (productStart + 1) * 4
                destinationRow[second + 0] = sourceRow[second + 0]
                destinationRow[second + 1] = sourceRow[second + 1]
                destinationRow[second + 2] = sourceRow[second + 2]
                destinationRow[second + 3] = 208
            }
        }
    }
}

func run() throws {
    guard CommandLine.arguments.count == 3 else { throw ProcessorError.usage }
    let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
    let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
    try? FileManager.default.removeItem(at: outputURL)

    let asset = AVURLAsset(url: inputURL)
    guard let track = asset.tracks(withMediaType: .video).first else {
        throw ProcessorError.noVideoTrack
    }

    let width = Int(track.naturalSize.width.rounded())
    let height = Int(track.naturalSize.height.rounded())
    let nominalFPS = track.nominalFrameRate > 0 ? Double(track.nominalFrameRate) : 24.0
    let duration = CMTimeGetSeconds(asset.duration)
    let estimatedFrames = max(1, Int((duration * nominalFPS).rounded()))

    let reader = try AVAssetReader(asset: asset)
    let readerOutput = AVAssetReaderTrackOutput(
        track: track,
        outputSettings: [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
            kCVPixelBufferIOSurfacePropertiesKey as String: [:]
        ]
    )
    readerOutput.alwaysCopiesSampleData = false
    guard reader.canAdd(readerOutput) else { throw ProcessorError.cannotAddReaderOutput }
    reader.add(readerOutput)

    var audioReaderOutput: AVAssetReaderTrackOutput?
    // Direct multi-track writing can deadlock under AVAssetWriter backpressure for slow Vision frames.
    // Keep it opt-in; the default workflow muxes the original audio in a fast passthrough second pass.
    let copyAudioInWriter = ProcessInfo.processInfo.environment["COPY_AUDIO_IN_WRITER"] == "1"
    let audioTrack = copyAudioInWriter ? asset.tracks(withMediaType: .audio).first : nil
    if let audioTrack {
        let output = AVAssetReaderTrackOutput(track: audioTrack, outputSettings: nil)
        output.alwaysCopiesSampleData = false
        if reader.canAdd(output) {
            reader.add(output)
            audioReaderOutput = output
        }
    }

    let writer = try AVAssetWriter(outputURL: outputURL, fileType: .mov)
    let useHEVCAlpha = ProcessInfo.processInfo.environment["HEVC_ALPHA"] == "1"
    let videoSettings: [String: Any]
    if useHEVCAlpha {
        videoSettings = [
            AVVideoCodecKey: AVVideoCodecType.hevcWithAlpha,
            AVVideoWidthKey: width,
            AVVideoHeightKey: height
        ]
    } else {
        videoSettings = [
            AVVideoCodecKey: AVVideoCodecType.proRes4444,
            AVVideoWidthKey: width,
            AVVideoHeightKey: height
        ]
    }
    let writerInput = AVAssetWriterInput(
        mediaType: .video,
        outputSettings: videoSettings
    )
    writerInput.expectsMediaDataInRealTime = false
    writerInput.transform = track.preferredTransform
    guard writer.canAdd(writerInput) else { throw ProcessorError.cannotAddWriterInput }
    writer.add(writerInput)

    var audioWriterInput: AVAssetWriterInput?
    if let audioTrack, let firstFormat = audioTrack.formatDescriptions.first {
        let formatHint = firstFormat as! CMFormatDescription
        let input = AVAssetWriterInput(mediaType: .audio, outputSettings: nil, sourceFormatHint: formatHint)
        input.expectsMediaDataInRealTime = false
        if writer.canAdd(input) {
            writer.add(input)
            audioWriterInput = input
        }
    }

    let adaptor = AVAssetWriterInputPixelBufferAdaptor(
        assetWriterInput: writerInput,
        sourcePixelBufferAttributes: [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
            kCVPixelBufferWidthKey as String: width,
            kCVPixelBufferHeightKey as String: height,
            kCVPixelBufferIOSurfacePropertiesKey as String: [:]
        ]
    )

    guard writer.startWriting() else {
        throw ProcessorError.cannotStartWriter(writer.error?.localizedDescription ?? "unknown error")
    }
    writer.startSession(atSourceTime: .zero)
    guard reader.startReading() else {
        throw ProcessorError.cannotStartReader(reader.error?.localizedDescription ?? "unknown error")
    }

    var pendingAudioSample = audioReaderOutput?.copyNextSampleBuffer()
    var copiedAudioSamples = 0

    let ciContext = CIContext(options: [
        .cacheIntermediates: false,
        .workingColorSpace: CGColorSpace(name: CGColorSpace.sRGB) as Any,
        .outputColorSpace: CGColorSpace(name: CGColorSpace.sRGB) as Any
    ])
    let outputBounds = CGRect(x: 0, y: 0, width: width, height: height)
    let transparent = CIImage(color: CIColor.clear).cropped(to: outputBounds)
    let outputColorSpace = CGColorSpace(name: CGColorSpace.sRGB)!
    let repairLowerLeftProductZone = ProcessInfo.processInfo.environment["REPAIR_LOWER_LEFT_PRODUCT_ZONE"] == "1"
    let alphaErodeRadius = Double(ProcessInfo.processInfo.environment["ALPHA_ERODE_RADIUS"] ?? "0") ?? 0
    let alphaEdgeContrast = Double(ProcessInfo.processInfo.environment["ALPHA_EDGE_CONTRAST"] ?? "1") ?? 1
    let alphaUniformEdgeSigma = Double(ProcessInfo.processInfo.environment["ALPHA_UNIFORM_EDGE_SIGMA"] ?? "0") ?? 0
    let alphaContourSmoothSigma = Double(ProcessInfo.processInfo.environment["ALPHA_CONTOUR_SMOOTH_SIGMA"] ?? "0") ?? 0
    let precomputedMaskDirectory = ProcessInfo.processInfo.environment["PRECOMPUTED_MASK_DIR"]
    let preservePremultipliedEdgeRGB = ProcessInfo.processInfo.environment["PRESERVE_PREMULTIPLIED_EDGE_RGB"] == "1"

    var frameIndex = 0
    while let sample = readerOutput.copyNextSampleBuffer() {
        let videoTimestamp = CMSampleBufferGetPresentationTimeStamp(sample)
        if let audioWriterInput, let audioReaderOutput {
            while let audioSample = pendingAudioSample,
                  CMTimeCompare(CMSampleBufferGetPresentationTimeStamp(audioSample), videoTimestamp) <= 0 {
                try waitForWriter(audioWriterInput, writer: writer)
                guard audioWriterInput.append(audioSample) else {
                    throw ProcessorError.appendFailed(writer.error?.localizedDescription ?? "audio append failed")
                }
                copiedAudioSamples += 1
                pendingAudioSample = audioReaderOutput.copyNextSampleBuffer()
            }
        }

        try autoreleasepool {
            guard let sourceBuffer = CMSampleBufferGetImageBuffer(sample) else {
                throw ProcessorError.missingPixelBuffer
            }

            let source = CIImage(cvPixelBuffer: sourceBuffer).cropped(to: outputBounds)

            var mask: CIImage
            if let precomputedMaskDirectory {
                let maskName = String(format: "mask_%03d.png", frameIndex)
                let maskURL = URL(fileURLWithPath: precomputedMaskDirectory, isDirectory: true)
                    .appendingPathComponent(maskName)
                guard let loadedMask = CIImage(contentsOf: maskURL, options: [.applyOrientationProperty: true]) else {
                    throw ProcessorError.cannotCreateAnalysisImage(frameIndex)
                }
                mask = loadedMask.cropped(to: outputBounds)
            } else {
                // Vision's direct CVPixelBuffer path can misclassify dark engraved details on
                // very light products, producing transparent bites around logos. Rendering the
                // decoded frame to a color-managed CGImage first gives the foreground request a
                // stable RGB representation and keeps those low-contrast product regions intact.
                guard let analysisImage = ciContext.createCGImage(source, from: outputBounds) else {
                    throw ProcessorError.cannotCreateAnalysisImage(frameIndex)
                }

                let request = VNGenerateForegroundInstanceMaskRequest()
                let requestHandler = VNImageRequestHandler(cgImage: analysisImage, orientation: .up, options: [:])
                try requestHandler.perform([request])
                guard let observation = request.results?.first else {
                    throw ProcessorError.noForeground(frameIndex)
                }

                let rawMaskBuffer = try observation.generateScaledMaskForImage(
                    forInstances: observation.allInstances,
                    from: requestHandler
                )
                mask = CIImage(cvPixelBuffer: rawMaskBuffer).cropped(to: outputBounds)

                // Close only tiny false holes while retaining real openings such as the ear-hook centers.
                mask = mask
                    .applyingFilter("CIMorphologyMaximum", parameters: ["inputRadius": 3.0])
                    .applyingFilter("CIMorphologyMinimum", parameters: ["inputRadius": 3.0])
                    .cropped(to: outputBounds)
                if alphaErodeRadius > 0 {
                    mask = mask
                        .applyingFilter("CIMorphologyMinimum", parameters: ["inputRadius": alphaErodeRadius])
                        .cropped(to: outputBounds)
                }
                if alphaUniformEdgeSigma > 0 {
                    // Vision can produce a different feather width on opposite sides of the
                    // stylus and between white/black source-background sections. Collapse the
                    // mask around its 50% contour, then add one controlled feather so every
                    // frame uses the same narrow anti-aliased transition.
                    if alphaContourSmoothSigma > 0 {
                        // Smooth small frame-to-frame contour ripples before thresholding. Since
                        // the next step keeps the 50% contour, this removes scalloping without
                        // growing the mask back into the contaminated source-background edge.
                        mask = mask
                            .clampedToExtent()
                            .applyingFilter("CIGaussianBlur", parameters: [kCIInputRadiusKey: alphaContourSmoothSigma])
                            .cropped(to: outputBounds)
                    }
                    let thresholdScale = 64.0
                    let thresholdBias = -(thresholdScale * 0.5 - 0.5)
                    mask = mask
                        .applyingFilter("CIColorMatrix", parameters: [
                            "inputRVector": CIVector(x: thresholdScale, y: 0, z: 0, w: 0),
                            "inputGVector": CIVector(x: thresholdScale, y: 0, z: 0, w: 0),
                            "inputBVector": CIVector(x: thresholdScale, y: 0, z: 0, w: 0),
                            "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
                            "inputBiasVector": CIVector(x: thresholdBias, y: thresholdBias, z: thresholdBias, w: 0)
                        ])
                        .applyingFilter("CIColorClamp", parameters: [
                            "inputMinComponents": CIVector(x: 0, y: 0, z: 0, w: 0),
                            "inputMaxComponents": CIVector(x: 1, y: 1, z: 1, w: 1)
                        ])
                        .clampedToExtent()
                        .applyingFilter("CIGaussianBlur", parameters: [kCIInputRadiusKey: alphaUniformEdgeSigma])
                        .cropped(to: outputBounds)
                }
            }
            if alphaEdgeContrast > 1 {
                mask = mask
                    .applyingFilter("CIColorControls", parameters: [
                        kCIInputContrastKey: alphaEdgeContrast,
                        kCIInputBrightnessKey: 0.0
                    ])
                    .cropped(to: outputBounds)
            }

            let foreground = source.applyingFilter("CIBlendWithMask", parameters: [
                kCIInputBackgroundImageKey: transparent,
                kCIInputMaskImageKey: mask
            ]).cropped(to: outputBounds)

            guard let pool = adaptor.pixelBufferPool else {
                throw ProcessorError.cannotAllocateOutputBuffer
            }
            var outputBuffer: CVPixelBuffer?
            guard CVPixelBufferPoolCreatePixelBuffer(nil, pool, &outputBuffer) == kCVReturnSuccess,
                  let outputBuffer else {
                throw ProcessorError.cannotAllocateOutputBuffer
            }

            ciContext.render(
                foreground,
                to: outputBuffer,
                bounds: outputBounds,
                colorSpace: outputColorSpace
            )
            if repairLowerLeftProductZone {
                repairStylusBodyAlpha(source: sourceBuffer, destination: outputBuffer)
            }
            removeBackgroundMatte(
                source: sourceBuffer,
                destination: outputBuffer,
                preservePremultipliedEdgeRGB: preservePremultipliedEdgeRGB
            )

            try waitForWriter(writerInput, writer: writer)
            let timestamp = CMSampleBufferGetPresentationTimeStamp(sample)
            guard adaptor.append(outputBuffer, withPresentationTime: timestamp) else {
                throw ProcessorError.appendFailed(writer.error?.localizedDescription ?? "unknown error")
            }
        }

        frameIndex += 1
        if frameIndex == 1 || frameIndex % 10 == 0 || frameIndex == estimatedFrames {
            let percent = min(100.0, Double(frameIndex) / Double(estimatedFrames) * 100.0)
            print(String(format: "frame %d/%d (%.1f%%)", frameIndex, estimatedFrames, percent))
            fflush(stdout)
        }
    }

    writerInput.markAsFinished()
    if let audioReaderOutput, let audioWriterInput {
        while let sample = pendingAudioSample {
            try waitForWriter(audioWriterInput, writer: writer)
            guard audioWriterInput.append(sample) else {
                throw ProcessorError.appendFailed(writer.error?.localizedDescription ?? "audio append failed")
            }
            copiedAudioSamples += 1
            pendingAudioSample = audioReaderOutput.copyNextSampleBuffer()
        }
        audioWriterInput.markAsFinished()
        print("Copied \(copiedAudioSamples) audio samples")
    }

    if reader.status == .failed {
        throw ProcessorError.readerFailed(reader.error?.localizedDescription ?? "unknown error")
    }

    let semaphore = DispatchSemaphore(value: 0)
    writer.finishWriting { semaphore.signal() }
    semaphore.wait()
    guard writer.status == .completed else {
        throw ProcessorError.writerFailed(writer.error?.localizedDescription ?? "unknown error")
    }

    print("Wrote \(frameIndex) frames to \(outputURL.path)")
}

do {
    try run()
} catch {
    fputs("ERROR: \(error)\n", stderr)
    exit(1)
}
