import Foundation
import AVFoundation
import CoreVideo
import ImageIO
import UniformTypeIdentifiers

guard CommandLine.arguments.count == 3 else {
    fputs("Usage: verify_alpha <input.mov> <output-dir>\n", stderr)
    exit(2)
}

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputDir = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
try FileManager.default.createDirectory(at: outputDir, withIntermediateDirectories: true)

func writeBGRA(_ data: Data, width: Int, height: Int, rowBytes: Int, to url: URL) throws {
    guard let provider = CGDataProvider(data: data as CFData),
          let cg = CGImage(
            width: width,
            height: height,
            bitsPerComponent: 8,
            bitsPerPixel: 32,
            bytesPerRow: rowBytes,
            space: CGColorSpace(name: CGColorSpace.sRGB)!,
            bitmapInfo: CGBitmapInfo.byteOrder32Little.union(
                CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedFirst.rawValue)
            ),
            provider: provider,
            decode: nil,
            shouldInterpolate: true,
            intent: .defaultIntent
          ) else {
        throw NSError(domain: "verify_alpha", code: 1)
    }
    guard let destination = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil) else {
        throw NSError(domain: "verify_alpha", code: 2)
    }
    CGImageDestinationAddImage(destination, cg, nil)
    guard CGImageDestinationFinalize(destination) else {
        throw NSError(domain: "verify_alpha", code: 3)
    }
}

let asset = AVURLAsset(url: inputURL)
guard let track = asset.tracks(withMediaType: .video).first else {
    fputs("No video track\n", stderr)
    exit(3)
}

let reader = try AVAssetReader(asset: asset)
let output = AVAssetReaderTrackOutput(track: track, outputSettings: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
    kCVPixelBufferIOSurfacePropertiesKey as String: [:]
])
output.alwaysCopiesSampleData = false
reader.add(output)
guard reader.startReading() else {
    throw reader.error ?? NSError(domain: "verify_alpha", code: 4)
}

let expectedFrames = max(1, Int((CMTimeGetSeconds(asset.duration) * Double(track.nominalFrameRate)).rounded()))
let lastFrame = expectedFrames - 1
let dumpAllFrames = ProcessInfo.processInfo.environment["DUMP_ALL_FRAMES"] == "1"
let targetFrames: Set<Int> = dumpAllFrames
    ? Set(0...lastFrame)
    : [0, lastFrame / 4, lastFrame / 2, lastFrame * 3 / 4, lastFrame]
var frameIndex = 0
var sampledPixels = 0
var transparentPixels = 0
var partialPixels = 0
var opaquePixels = 0
var minAlpha = 255
var maxAlpha = 0
var firstPTS = CMTime.invalid
var lastPTS = CMTime.invalid

while let sample = output.copyNextSampleBuffer() {
    guard let buffer = CMSampleBufferGetImageBuffer(sample) else { continue }
    let pts = CMSampleBufferGetPresentationTimeStamp(sample)
    if !firstPTS.isValid { firstPTS = pts }
    lastPTS = pts

    CVPixelBufferLockBaseAddress(buffer, .readOnly)
    if let base = CVPixelBufferGetBaseAddress(buffer) {
        let width = CVPixelBufferGetWidth(buffer)
        let height = CVPixelBufferGetHeight(buffer)
        let rowBytes = CVPixelBufferGetBytesPerRow(buffer)
        let bytes = base.assumingMemoryBound(to: UInt8.self)
        for y in stride(from: 0, to: height, by: 4) {
            let row = bytes.advanced(by: y * rowBytes)
            for x in stride(from: 0, to: width, by: 4) {
                let alpha = Int(row[x * 4 + 3])
                sampledPixels += 1
                minAlpha = min(minAlpha, alpha)
                maxAlpha = max(maxAlpha, alpha)
                if alpha == 0 { transparentPixels += 1 }
                else if alpha == 255 { opaquePixels += 1 }
                else { partialPixels += 1 }
            }
        }
    }
    CVPixelBufferUnlockBaseAddress(buffer, .readOnly)

    if targetFrames.contains(frameIndex) {
        CVPixelBufferLockBaseAddress(buffer, .readOnly)
        let width = CVPixelBufferGetWidth(buffer)
        let height = CVPixelBufferGetHeight(buffer)
        let rowBytes = CVPixelBufferGetBytesPerRow(buffer)
        let byteCount = rowBytes * height
        guard let base = CVPixelBufferGetBaseAddress(buffer) else {
            throw NSError(domain: "verify_alpha", code: 6)
        }
        let rgba = Data(bytes: base, count: byteCount)
        var alpha = Data(count: byteCount)
        var checker = Data(count: byteCount)
        rgba.withUnsafeBytes { sourceRaw in
            alpha.withUnsafeMutableBytes { alphaRaw in
                checker.withUnsafeMutableBytes { checkerRaw in
                    let source = sourceRaw.bindMemory(to: UInt8.self)
                    let alphaBytes = alphaRaw.bindMemory(to: UInt8.self)
                    let checkerBytes = checkerRaw.bindMemory(to: UInt8.self)
                    for y in 0..<height {
                        for x in 0..<width {
                            let offset = y * rowBytes + x * 4
                            let a = Int(source[offset + 3])
                            alphaBytes[offset + 0] = UInt8(a)
                            alphaBytes[offset + 1] = UInt8(a)
                            alphaBytes[offset + 2] = UInt8(a)
                            alphaBytes[offset + 3] = 255

                            let tile = ((x / 28) + (y / 28)) & 1
                            let background = tile == 0 ? 209 : 158
                            let inverse = 255 - a
                            checkerBytes[offset + 0] = UInt8(min(255, Int(source[offset + 0]) + background * inverse / 255))
                            checkerBytes[offset + 1] = UInt8(min(255, Int(source[offset + 1]) + background * inverse / 255))
                            checkerBytes[offset + 2] = UInt8(min(255, Int(source[offset + 2]) + background * inverse / 255))
                            checkerBytes[offset + 3] = 255
                        }
                    }
                }
            }
        }
        CVPixelBufferUnlockBaseAddress(buffer, .readOnly)
        let suffix = String(format: "%03d", frameIndex)
        try writeBGRA(rgba, width: width, height: height, rowBytes: rowBytes, to: outputDir.appendingPathComponent("rgba_\(suffix).png"))
        try writeBGRA(alpha, width: width, height: height, rowBytes: rowBytes, to: outputDir.appendingPathComponent("alpha_\(suffix).png"))
        try writeBGRA(checker, width: width, height: height, rowBytes: rowBytes, to: outputDir.appendingPathComponent("checker_\(suffix).png"))
    }
    frameIndex += 1
}

if reader.status == .failed {
    throw reader.error ?? NSError(domain: "verify_alpha", code: 5)
}

let duration = CMTimeGetSeconds(asset.duration)
let firstSeconds = firstPTS.isValid ? CMTimeGetSeconds(firstPTS) : -1
let lastSeconds = lastPTS.isValid ? CMTimeGetSeconds(lastPTS) : -1
print("frames=\(frameIndex)")
print(String(format: "duration=%.6f first_pts=%.6f last_pts=%.6f", duration, firstSeconds, lastSeconds))
print("sampled_pixels=\(sampledPixels) alpha_min=\(minAlpha) alpha_max=\(maxAlpha)")
print("alpha_zero=\(transparentPixels) alpha_partial=\(partialPixels) alpha_opaque=\(opaquePixels)")
