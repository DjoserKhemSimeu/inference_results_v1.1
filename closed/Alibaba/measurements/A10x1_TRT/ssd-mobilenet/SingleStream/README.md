To run this benchmark, first follow the setup steps in `closed/Alibaba/README.md`. Then to generate the TensorRT engines and run the harness:

```
make generate_engines RUN_ARGS="--benchmarks=ssd-mobilenet --scenarios=SingleStream"
make run_harness RUN_ARGS="--benchmarks=ssd-mobilenet --scenarios=SingleStream --test_mode=AccuracyOnly"
make run_harness RUN_ARGS="--benchmarks=ssd-mobilenet --scenarios=SingleStream --test_mode=PerformanceOnly"
```

For more details, please refer to `closed/Alibaba/README.md`.