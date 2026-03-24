using App.Benchmark;
using App.Models;

Console.WriteLine("=== 2D Benchmark ===");

var polarPoints = Benchmark2D.GeneratePolarPoints(100_000);

var cartesianPoints = new CartesianPoint2D[polarPoints.Length];
for (int i = 0; i < polarPoints.Length; i++)
{
    cartesianPoints[i] = CartesianPoint2D.FromPolar(polarPoints[i]);
}

var polarResult = Benchmark2D.BenchmarkPolar(polarPoints);
Console.WriteLine($"Polar: {polarResult.elapsedMs} ms, sum={polarResult.sum}");

var cartesianResult = Benchmark2D.BenchmarkCartesian(cartesianPoints);
Console.WriteLine($"Cartesian: {cartesianResult.elapsedMs} ms, sum={cartesianResult.sum}");


Console.WriteLine("\n=== 3D Benchmark ===");

var (sphericalFirst, sphericalSecond) = Benchmark3D.GenerateSphericalPairs(100_000);

var cartesian3DFirst = new CartesianPoint3D[sphericalFirst.Length];
var cartesian3DSecond = new CartesianPoint3D[sphericalSecond.Length];
for (int i = 0; i < sphericalFirst.Length; i++)
{
    cartesian3DFirst[i] = CartesianPoint3D.FromSpherical(sphericalFirst[i]);
    cartesian3DSecond[i] = CartesianPoint3D.FromSpherical(sphericalSecond[i]);
}

var chordResult = Benchmark3D.BenchmarkChord(sphericalFirst, sphericalSecond);
Console.WriteLine($"Chord distance: {chordResult.elapsedMs} ms, sum={chordResult.sum}");

var arcResult = Benchmark3D.BenchmarkArc(sphericalFirst, sphericalSecond);
Console.WriteLine($"Arc distance: {arcResult.elapsedMs} ms, sum={arcResult.sum}");

var cartesian3DResult = Benchmark3D.BenchmarkCartesian(cartesian3DFirst, cartesian3DSecond);
Console.WriteLine($"Cartesian 3D: {cartesian3DResult.elapsedMs} ms, sum={cartesian3DResult.sum}");