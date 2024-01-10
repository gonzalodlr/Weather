module Demo {
    struct Measurement {
        string tower; // Tower id.
        float windSpeed; // Knots.
        short windDirection; // Degrees.
        float temperature; // Degrees Celsius.
    };
    interface Monitor {
        void report(Measurement m);
    };
};