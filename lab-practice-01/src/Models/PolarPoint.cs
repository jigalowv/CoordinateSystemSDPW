namespace App.Models;

public sealed class PolarPoint
{
    private readonly double _radius;
    private readonly double _angle;

    public double Radius => _radius;
    public double Angle => _angle;

    public PolarPoint(
        double radius, 
        double angle)
    {
        _radius = radius;
        _angle = angle;
    }

    public static PolarPoint FromCartesian(CartesianPoint2D p)
    {
        var radius = Math.Sqrt(p.X * p.X + p.Y * p.Y);
        var angle = Math.Atan2(p.Y, p.X);

        return new PolarPoint(radius, angle);
    }
}