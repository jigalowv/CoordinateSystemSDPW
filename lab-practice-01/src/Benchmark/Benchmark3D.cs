using System;
using System.Diagnostics;
using System.Linq;
using App.Extensions;
using App.Models;

namespace App.Benchmark;

public static class Benchmark3D
{
    private static readonly Random Random = new Random();

    public static (SphericalPoint[] first, SphericalPoint[] second) GenerateSphericalPairs(int count, double maxRadius = 1000)
    {
        var first = new SphericalPoint[count];
        var second = new SphericalPoint[count];

        for (int i = 0; i < count; i++)
        {
            double radius = Random.NextDouble() * maxRadius;
            // Випадкові кути
            double az1 = Random.NextDouble() * 2 * Math.PI;
            double pol1 = Random.NextDouble() * Math.PI;
            double az2 = Random.NextDouble() * 2 * Math.PI;
            double pol2 = Random.NextDouble() * Math.PI;

            first[i] = new SphericalPoint(radius, az1, pol1);
            second[i] = new SphericalPoint(radius, az2, pol2); // той же radius
        }

        return (first, second);
    }

    public static CartesianPoint3D[] ToCartesian(SphericalPoint[] points)
    {
        return points.Select(p => CartesianPoint3D.FromSpherical(p)).ToArray();
    }

    public static (double sum, long elapsedMs) BenchmarkChord(SphericalPoint[] first, SphericalPoint[] second)
    {
        if (first.Length != second.Length)
            throw new ArgumentException("Arrays must have the same length");

        var sw = Stopwatch.StartNew();
        double sum = 0;
        for (int i = 0; i < first.Length; i++)
        {
            sum += first[i].DistanceChord(second[i]);
        }
        sw.Stop();
        return (sum, sw.ElapsedMilliseconds);
    }

    public static (double sum, long elapsedMs) BenchmarkArc(SphericalPoint[] first, SphericalPoint[] second)
    {
        if (first.Length != second.Length)
            throw new ArgumentException("Arrays must have the same length");

        var sw = Stopwatch.StartNew();
        double sum = 0;
        for (int i = 0; i < first.Length; i++)
        {
            sum += first[i].DistanceArc(second[i]);
        }
        sw.Stop();
        return (sum, sw.ElapsedMilliseconds);
    }

    public static (double sum, long elapsedMs) BenchmarkCartesian(CartesianPoint3D[] first, CartesianPoint3D[] second)
    {
        if (first.Length != second.Length)
            throw new ArgumentException("Arrays must have the same length");

        var sw = Stopwatch.StartNew();
        double sum = 0;
        for (int i = 0; i < first.Length; i++)
        {
            sum += first[i].Distance(second[i]);
        }
        sw.Stop();
        return (sum, sw.ElapsedMilliseconds);
    }
}