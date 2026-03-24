using App.Models;

namespace App.Extensions;

public static class DistanceUtils
{
    public static double Distance(
        this CartesianPoint2D from, 
        CartesianPoint2D to)
    {
        var dX = to.X - from.X;
        var dY = to.Y - from.Y;

        var distance = Math.Sqrt(dX * dX + dY * dY);

        return distance;
    }

    public static double Distance(
        this CartesianPoint3D from, 
        CartesianPoint3D to)
    {
        var dX = to.X - from.X;
        var dY = to.Y - from.Y;
        var dZ = to.Z - from.Z;

        var distance = Math.Sqrt(dX * dX + dY * dY + dZ * dZ);

        return distance;
    }

    public static double Distance(
        this PolarPoint from,
        PolarPoint to)
    {
        return Math.Sqrt(
            from.Radius * from.Radius + to.Radius * to.Radius
            - 2 * from.Radius * to.Radius * Math.Cos(from.Angle - to.Angle)
        );
    }

    public static double DistanceArc(
        this SphericalPoint from, 
        SphericalPoint to)
    {
        if (!from.Radius.AlmostEquals(to.Radius))
            throw new ArgumentException("Radiuses must equal");

        var r = from.Radius;
        var delta = from.PolarAngle - to.PolarAngle;

        return r * Math.Acos(
            Math.Sin(from.Azimuth) * Math.Sin(to.Azimuth) 
            * Math.Cos(delta)
            + Math.Cos(from.Azimuth) * Math.Cos(to.Azimuth)
        );
    }

    public static double DistanceChord(
        this SphericalPoint from, 
        SphericalPoint to)
    {
        var delta = from.Azimuth - to.Azimuth;

        return Math.Sqrt(
            from.Radius * from.Radius + to.Radius * to.Radius
            - 2 * from.Radius * to.Radius 
            * (Math.Sin(from.PolarAngle) * Math.Sin(to.PolarAngle) 
            * Math.Cos(delta) 
            + Math.Cos(from.PolarAngle) * Math.Cos(to.PolarAngle))
        );
    }
}