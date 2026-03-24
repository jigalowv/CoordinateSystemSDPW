namespace App.Extensions;

public static class FloatingPointUtils
{
    public static bool AlmostEquals(this double value, double to, double eps = 1e-9)
    {
        return Math.Abs(value - to) < eps;
    }
}