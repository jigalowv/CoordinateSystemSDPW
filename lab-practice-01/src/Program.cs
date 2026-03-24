using App.Benchmark;
using App.Models;

Console.WriteLine("=== Проверка преобразований 2D ===");

var cart2D = new CartesianPoint2D(3, 4);
var polar = new PolarPoint(5, Math.Atan2(4, 3));

var polarFromCart = PolarPoint.FromCartesian(cart2D);
var cartFromPolar = CartesianPoint2D.FromPolar(polarFromCart);

Console.WriteLine($"CartesianPoint2D: x={cart2D.X}, y={cart2D.Y}");
Console.WriteLine($"-> Converted to PolarPoint: radius={polarFromCart.Radius:F4}, angle={polarFromCart.Angle:F4}");
Console.WriteLine($"-> Converted back to CartesianPoint2D: x={cartFromPolar.X:F4}, y={cartFromPolar.Y:F4}");

var cartFromPolarDirect = CartesianPoint2D.FromPolar(polar);
var polarFromCartDirect = PolarPoint.FromCartesian(cartFromPolarDirect);

Console.WriteLine($"PolarPoint: radius={polar.Radius}, angle={polar.Angle:F4}");
Console.WriteLine($"-> Converted to CartesianPoint2D: x={cartFromPolarDirect.X:F4}, y={cartFromPolarDirect.Y:F4}");
Console.WriteLine($"-> Converted back to PolarPoint: radius={polarFromCartDirect.Radius:F4}, angle={polarFromCartDirect.Angle:F4}");

Console.WriteLine("\n=== Проверка преобразований 3D ===");

var cart3D = new CartesianPoint3D(2, 3, 6);
var spherical = new SphericalPoint(Math.Sqrt(2*2 + 3*3 + 6*6), Math.Atan2(3, 2), Math.Acos(6 / Math.Sqrt(2*2 + 3*3 + 6*6)));

var sphericalFromCart = SphericalPoint.FromCartesian(cart3D);
var cartFromSpherical = CartesianPoint3D.FromSpherical(sphericalFromCart);

Console.WriteLine($"CartesianPoint3D: x={cart3D.X}, y={cart3D.Y}, z={cart3D.Z}");
Console.WriteLine($"-> Converted to SphericalPoint: radius={sphericalFromCart.Radius:F4}, azimuth={sphericalFromCart.Azimuth:F4}, polarAngle={sphericalFromCart.PolarAngle:F4}");
Console.WriteLine($"-> Converted back to CartesianPoint3D: x={cartFromSpherical.X:F4}, y={cartFromSpherical.Y:F4}, z={cartFromSpherical.Z:F4}");

var cartFromSphericalDirect = CartesianPoint3D.FromSpherical(spherical);
var sphericalFromCartDirect = SphericalPoint.FromCartesian(cartFromSphericalDirect);

Console.WriteLine($"SphericalPoint: radius={spherical.Radius:F4}, azimuth={spherical.Azimuth:F4}, polarAngle={spherical.PolarAngle:F4}");
Console.WriteLine($"-> Converted to CartesianPoint3D: x={cartFromSphericalDirect.X:F4}, y={cartFromSphericalDirect.Y:F4}, z={cartFromSphericalDirect.Z:F4}");
Console.WriteLine($"-> Converted back to SphericalPoint: radius={sphericalFromCartDirect.Radius:F4}, azimuth={sphericalFromCartDirect.Azimuth:F4}, polarAngle={sphericalFromCartDirect.PolarAngle:F4}");

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