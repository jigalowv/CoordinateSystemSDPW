using System.Diagnostics;
using App.Extensions;
using App.Models;

namespace App.Benchmark;

public static class Benchmark2D
{
    private static readonly Random Random = new Random();

    public static PolarPoint[] GeneratePolarPoints(int count, double maxRadius = 1000)
    {
        var points = new PolarPoint[count];
        for (int i = 0; i < count; i++)
        {
            double radius = Random.NextDouble() * maxRadius;
            double angle = Random.NextDouble() * 2 * Math.PI;
            points[i] = new PolarPoint(radius, angle);
        }
        return points;
    }

    public static CartesianPoint2D[] ToCartesian(PolarPoint[] polarPoints)
    {
        return polarPoints.Select(CartesianPoint2D.FromPolar).ToArray();
    }

    public static (double sum, long elapsedMs) BenchmarkPolar(PolarPoint[] points)
    {
        var sw = Stopwatch.StartNew();
        double sum = 0;
        for (int i = 0; i < points.Length - 1; i++)
        {
            sum += points[i].Distance(points[i + 1]);
        }
        sw.Stop();
        return (sum, sw.ElapsedMilliseconds);
    }

    public static (double sum, long elapsedMs) BenchmarkCartesian(CartesianPoint2D[] points)
    {
        var sw = Stopwatch.StartNew();
        double sum = 0;
        for (int i = 0; i < points.Length - 1; i++)
        {
            sum += points[i].Distance(points[i + 1]);
        }
        sw.Stop();
        return (sum, sw.ElapsedMilliseconds);
    }
}