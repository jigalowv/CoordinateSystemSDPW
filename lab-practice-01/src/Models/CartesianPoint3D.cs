namespace App.Models;

public sealed class CartesianPoint3D
{
    public readonly double _x;
    public readonly double _y;
    public readonly double _z;  

    public double X => _x;
    public double Y => _y;
    public double Z => _z;   

    public CartesianPoint3D(
        double x, 
        double y, 
        double z)
    {
        _x = x;
        _y = y;
        _z = z;
    }

    public static CartesianPoint3D FromSpherical(SphericalPoint p)
    {
        var x = p.Radius * Math.Sin(p.PolarAngle) * Math.Cos(p.Azimuth);
        var y = p.Radius * Math.Sin(p.PolarAngle) * Math.Sin(p.Azimuth);
        var z = p.Radius * Math.Cos(p.PolarAngle);

        return new CartesianPoint3D(x, y, z);
    }
}