#include <iostream>

struct Point
{
    int x;
    int y;

    Point(int _x, int _y)
    {
        x = _x;
        y = _y;
    }

    void print()
    {
        std::cout << "X is " << x << ", Y is " << y << std::endl;
    }
};

int main()
{
    Point p(1, 2);
    p.print();

    double* d = reinterpret_cast<double*>(&p);

    *d = 100;

    p.print();
}