namespace App.Models;

public sealed class SphericalPoint
{
    private readonly double _radius;
    private readonly double _azimuth;
    private readonly double _polarAngle;

    public double Radius => _radius;
    public double Azimuth => _azimuth;
    public double PolarAngle => _polarAngle;

    public SphericalPoint(
        double radius, 
        double azimuth,
        double polarAngle)
    {
        _radius = radius;
        _azimuth = azimuth;
        _polarAngle = polarAngle;
    }

    public static SphericalPoint FromCartesian(CartesianPoint3D p)
    {
        var radius = Math.Sqrt(p.X * p.X + p.Y * p.Y + p.Z * p.Z);
        var azimuth = Math.Atan2(p.Y, p.X);
        var polarAngle = Math.Acos(p.Z / radius);

        return new SphericalPoint(radius, azimuth, polarAngle);
    }
}