namespace App.Models;

public sealed class CartesianPoint2D
{
    private readonly double _x;
    private readonly double _y;

    public double X => _x;
    public double Y => _y;
    
    public CartesianPoint2D(
        double x, 
        double y)
    {
        _x = x;
        _y = y;
    }

    public static CartesianPoint2D FromPolar(PolarPoint p)
    {
        var x = p.Radius * Math.Cos(p.Angle);
        var y = p.Radius * Math.Sin(p.Angle);

        return new CartesianPoint2D(x, y);
    }
}