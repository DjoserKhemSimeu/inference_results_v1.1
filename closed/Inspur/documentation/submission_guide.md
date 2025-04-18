# MLPerf Inference Submission Guide

---

This guide explains and goes through the steps to prepare everything for a valid MLPerf Inference submission. To be considered a valid submission, it must satisfy:

- [MLPerf Inference rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
- [MLPerf Submission rules](https://github.com/mlcommons/policies/blob/master/submission_rules.adoc)

Make sure that you check the rules for the latest updates. Most of this guide is generic and applicable to all MLPerf Inference submissions. If any part of this guide is specific to NVIDIA's submission or directory structure, it will be explicitly mentioned.

### Before you continue

Before you continue with your submission, here are some common issues or things to double check before you start the submission process:

### LoadGen RNG Seeds and Valid LoadGen Git Hashes

LoadGen RNG seeds are **released 2 weeks before the submission deadline** to prevent submitters from over-tuning on specific sets of seeds. The official seeds will be added to the official [mlperf.conf](https://github.com/mlcommons/inference/blob/master/mlperf.conf) file once this is announced.

**Keep an eye out for this announcement, as it will also include a specific set of commit hashes** of the [official MLPerf inference repository](https://github.com/mlcommons/inference) that are considered valid for the current submission round. **Any submission that does not use one of these commit hashes will not be considered a valid submission.**

If you are an NVIDIA submission partner, NVIDIA will make an announcement as part of the final codedrop on whether or not the commit hashes have been finalized, and whether or not you will need to take action to update the hash.

### Minimal Query Count

[MLPerf Inference rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#3-scenarios) require that each performance test to run for at least a minimum number of queries or samples to ensure sufficient statistical confidence in the reported metric. These settings are automatically applied if you use a valid submission commit hash of the official inference repo, **but make sure you do not accidentally overwrite these settings in your user.conf files**. Below is a summary of this requirement:

- Offline: at least 24576 samples.
- SingleStream: at least 1024 queries.
- Server: at least 270336 queries.

Refer to performance_tuning_guide.md for how to calculate expected inference test runtimes due to this requirement.

If you are an NVIDIA submission partner, no action is needed unless NVIDIA makes an announcement of a required change. In any other case, simply make sure that you do not overwrite the 'minimal query count' setting in your user.conf.

### Performance Sample Count

MLPerf Inference rules require that the Loadable Set size of the QSL, called `performance_sample_count`, to be at least a minimum threshold to avoid implicit caching effects. These settings are automatically applied if you use a valid submission commit hash, but submitters can override this value in their `user.conf` files, as long as the values are greater than the required minimum.

If you are an NVIDIA submission partner, no action is needed unless NVIDIA makes an announcement of a required change. In any other case, make sure that if you overwrite this value, that it is greater than the minimum.

### INVALID Results reported by LoadGen

If you see a result being reported as 'INVALID' in the LoadGen summary log, then that run (and its result) **cannot be used as part of your submission**. Please follow performance_tuning_guide.md to fix these errors.

### Directory Structures

The required directory structure for submission can be found in the [MLCommons Policies repository](https://github.com/mlcommons/policies/blob/master/submission_rules.adoc#inference-1). A visual representation of the directory structure as of 6/29/2021 is shown below:

```
closed/$(SUBMITTER)/
|-- code/
|   |-- [benchmark name]
|   |   `-- [implementation id]
|   |       `-- [code interface with loadgen and other necessary code]
|   `-- ...
|-- measurements/
|   |-- [system_desc_id]
|   |   |-- [benchmark_name]
|   |   |   |-- [scenario]
|   |   |   |   |-- [system_desc_id]_[implementation id]_[scenario].json
|   |   |   |   |-- README.md
|   |   |   |   |-- calibration_process.adoc
|   |   |   |   |-- mlperf.conf
|   |   |   |   `-- user.conf
|   |   |   `-- ...
|   |   `-- ...
|   `-- ...
|-- results/
|   |-- compliance_checker_log.txt # stdout of submission checker script
|   `-- [system_desc_id]
|       |-- [benchmark_name]
|       |   `-- [scenario]
|       |       |-- accuracy/
|       |       |   |-- accuracy.txt # stdout of reference accuracy script
|       |       |   |-- mlperf_log_accuracy.json # Truncated by truncate_accuracy script
|       |       |   |-- mlperf_log_detail.txt
|       |       |   `-- mlperf_log_summary.txt
|       |       `-- performance/
|       |           |-- ranging                             # (only needed if power submission)
|       |           |   |-- mlperf_log_detail.txt           # ranging run
|       |           |   |-- mlperf_log_summary.txt          # ranging run
|       |           |   `-- spl.txt                         # ranging run
|       |           |-- run_1/ # 1 run for all scenarios
|       |           |   |-- mlperf_log_detail.txt           # testing run
|       |           |   |-- mlperf_log_summary.txt          # testing run
|       |           |   |-- spl.txt                         # testing run (only needed if power submission)
|       |           `-- power                               # (only needed if power submission)
|       |               |-- client.json
|       |               |-- client.log
|       |               |-- ptd_logs.txt
|       |               |-- server.json
|       |               `-- server.log
|       `-- ...
|-- systems/
|   |-- [system_desc_id].json # combines hardware and software stack information
|   `-- ...
`-- compliance
    `-- [system_desc_id]
        |-- [benchmark_name]
        |   |-- [scenario]
        |   |   |-- [test_id]
        |   |   |   |-- verify_performance.txt
        |   |   |   |-- verify_accuracy.txt # For TEST01 only
        |   |   |-- accuracy/ # For TEST01 only
        |   |   |   |   |-- accuracy.txt # stdout of reference accuracy script
        |   |   |   |   |-- mlperf_log_accuracy.json # Truncated by truncate_accuracy script
        |   |   |   |   |-- baseline_accuracy.txt # only for TEST01 if accuracy check fails
        |   |   |   |   |-- compliance_accuracy.txt # only for TEST01 if accuracy check fails
        |   |   |   |   |-- mlperf_log_detail.txt
        |   |   |   |   `-- mlperf_log_summary.txt
        |   |   |   `-- performance/
        |   |   |       `-- run_1/ # 1 run for all scenarios
        |   |   |           |-- mlperf_log_detail.txt
        |   |   |           `-- mlperf_log_summary.txt
        |   |   `-- ...
        |   `-- ...
        `-- ...
```
Valid values for `benchmark_name` are:

- resnet50
- ssd-mobilenet
- ssd-resnet34
- rnnt
- bert-99
- bert-99.9
- dlrm-99
- dlrm-99.9
- 3d-unet-99
- 3d-unet-99.9

Valid values for `scenario` are:

- Offline
- Server
- SingleStream

Valid values of `test_id` are:

- TEST01
- TEST04-A
- TEST04-B
- TEST05

Other than required files, submitters can put any addition files as long as their naming and layout do not conflict with the required files.

### Benchmark code

Code for benchmark implementation and interfaces with LoadGen (including QSL and SUT implementations) should be placed under `code/[BENCHMARK]/[IMPLEMENTATION]`. The contents of this directory can be as simple as a copy of the reference implementation from the [MLCommons Inference repo](https://github.com/mlcommons/inference), or a from-scratch implementation as long as it satisfies the [model equivalence requirements](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#model-equivalence).

In NVIDIA's submission code, the codes under code can be used directly as is if you have an equivalent system. If you have a system with a different configuration, see the 'Prepping our repo for your machine' section in closed/NVIDIA/README.md to make the necessary modifications to fit your system. .

If you are an NVIDIA submission partner, you will need to change the submission to be under your company name:

- Move `closed/NVIDIA` to `closed/[your company name]`
- In your submission system descriptions (`closed/[company name]/systems/[system name].json`), change the 'submitter' field to your company name
- In `closed/[company name]/Makefile`, redefine the `SUBMITTER` variable to the correct value, or append `SUBMITTER=[your company name]` to all of your `make` commands when running the code

### Add System Descriptions

Under the `closed/[company name]/systems` directory, each submission system must have a system description file named `[system_name].json`. Below are the required fields in the system description JSON file. These entries must exist and cannot be empty strings.

- `accelerator_memory_capacity`
- `accelerator_model_name`
- `accelerators_per_node`
- `division`
- `framework`
- `host_memory_capacity`
- `host_processor_core_count`
- `host_processor_model_name`
- `host_processors_per_node`
- `host_storage_capacity`
- `host_storage_type`
- `number_of_nodes`
- `operating_system`
- `submitter`
- `status`
- `system_name`
- `system_type`

Below are the optional fields in the system description JSON. These entries can be empty strings if they do not apply to your system:

- `accelerator_frequency`
- `accelerator_host_interconnect`
- `accelerator_interconnect`
- `accelerator_interconnect_topology`
- `accelerator_memory_configuration`
- `accelerator_on-chip_memories`
- `cooling`
- `host_networking`
- `host_networking_topology`
- `host_memory_configuration`
- `host_processor_caches`
- `host_processor_frequency`
- `host_processor_interconnect`
- `hw_notes`
- `other_software_stack`
- `sw_notes`

In NVIDIA submission code, you can use one of the provided system description JSON files as a template. **Be sure to remove all other system description JSON files of systems you are not submitting with. This must be done *before* you submit your** submission.

### Update User Configurations (measurements, user.conf, and mlperf.conf)

MLPerf Inference submission rules require that you put the following files under `closed/[submitter]/measurements/[system_id]/[benchmark]/[scenario]`:

- `[system_desc_id]_[implementation_id]_[scenario].json`: a JSON file containing the following entries:
    - `input_data_types`: datatype of the input (i.e. fp16, int8, fp32, etc.)
    - `retraining`: `Y` if the weights are modified with retraining, `N` otherwise.
    - `starting_weights_filename`: the filename of the original reference weights (model) used in the implementation
    - `weight_data_types`: datatype of the weights (i.e. fp16, int8, fp32, etc.)
    - `weight_transformations`: transformations applied to the weights
- `README.md`: Markdown file containing instructions on how to run the specific benchmark
- `mlperf.conf`: LoadGen config file with rule complying settings. This must be an unmodified copy of the [official mlperf.conf file](https://github.com/mlcommons/inference/blob/master/mlperf.conf).
- `user.conf`: LoadGen config file with user settings. This includes options like 'target_qps', etc. See the comments in the [official mlperf.conf](https://github.com/mlcommons/inference/blob/master/mlperf.conf) for more information.
- `calibration_process.adoc`: Documentation about how post-training calibration/quantization is done.

In NVIDIA's submission code, **do NOT modify the files in the `measurements` directory directly**. In our submission, we generate these files automatically at runtime programmatically from the benchmark configuration files located in `configs/`. You will need to make the following changes in order:

1. Modify the `code/common/system_list.py` to only include the systems you plan on submitting with
2. Modify the config files under `configs/` to only include configurations for the systems you are submitting with
3. **Remove** the entire `measurements/` directory
4. Run `make generate_conf_files`. This will generate all the required measurements files.

### Update Result Logs

For each system-benchmark-scenario tuple, you will need to generate LoadGen logs for inference runs and place them under `results/[system ID]/[benchmark]/[scenario]/performance/run_[x]/` and `results[system ID]/[benchmark]/[scenario]/accuracy`. As of v1.0, a valid submission requires 1 performance log and 1 accuracy log per system-benchmark-scenario tuple.

For performance runs, the required files are `mlperf_log_summary.txt` and `mlperf_log_detail.txt` generated by LoadGen. The accuracy runs require both of these files as well, in addition to the `mlperf_log_accuracy.json` generated by LoadGen, and `accuracy.txt`, which contains the stdout log of running the official accuracy script on the `mlperf_log_accuracy.json` to compute the accuracy.

In NVIDIA submission code structure, follow the below instructions to generate the required files:

1. Remove any existing logs with `rm -rf build/logs`.
    1. If you would like to keep these logs for development purposes, back up this directory elsewhere beforehand, preferably outside of the project repo's directory (perhaps a separate drive specifically for storage).
2. Run all benchmarks and scenarios you would like to submit results in. Remember to pass in `--config_ver=default,high_accuracy` to make sure both accuracy targets are covered. If you are also submitting with Triton, add `triton` and `high_accuracy_triton` to the list of config versions.

```
$ make run RUN_ARGS="--benchmarks=... --scenarios=... --config_ver=default,high_accuracy[,triton,high_accuracy_triton]"
```

3. Run the accuracy tests as well by adding the `test_mode` flag:

```
$ make run_harness RUN_ARGS="--benchmarks=... --scenarios=... --config_ver=default,high_accuracy[,triton,high_accuracy_triton] --test_mode=AccuracyOnly"
```

4. Ensure that your system description JSON files from the 'System Descriptions' section exist in the `systems/` directory.
5. Run `make update_results`. This command will parse all logs in build/logs and insert them into results/
6. Continue to the next section, which describes how to run the compliance tests.

### Update Compliance Logs

After updating the `results/` directory (see previous section), you will need to generate 'compliance test logs' for each of the four different tests listed in the [Official MLPerf Inference Compliance Tests](https://github.com/mlcommons/inference/tree/master/compliance/nvidia). The tests are summarized below:

- `TEST01`: Samples and logs the SUT response randomly in Performance mode. This is to verify that the SUT generates the same outputs for the same set of inputs when the test mode is switched between PerformanceOnly and AccuracyOnly, as it is possible to cheat by generating garbage responses in PerformanceOnly mode, but performing the actual inference in AccuracyOnly mode.
    - This test may fail if your SUT has nondeterministic characteristics, such as running on different types of accelerators concurrently (i.e. GPU+DLA), or when the codepath has nondeterministic settings based on runtime factors (such as choosing different CUDA kernels based on specific characteristics of a batch, i.e. sparsity).
    - If your SUT has nondeterministic characteristics as described above, the MLPerf Inference rules require that the submitter provide an explanation and documentation of the nondeterministic behavior, and to manually check the accuracy of the Performance mode accuracy logs (see [TEST01 Part III](https://github.com/mlcommons/inference/tree/master/compliance/nvidia/TEST01#part-iii)). **Note: This is done automatically with the instructions described later.**
- `TEST04-A/B`: Checks the performance with the same sample P times compared to P unique samples. This is to detect if the SUT is possibly doing result caching. If this test fails, it means that performance when running inference on the same sample P times is significantly faster than the performance with P unique samples. **It is expected that this test will show INVALID in its result logs. You can ignore this.**
- `TEST05`: Runs the Performance mode inference run with a different set of random number generator seeds. This is to detect if the submitter hyper-tuned the SUT for a specific RNG seed.

**Important:** The way audit tests function is by placing an `audit.conf` file in the working directory that is automatically detected by LoadGen, and then used as a temporary setting override.

- If you had intentionally placed your own `audit.conf` in the working directory (`/work` within the container) before running the audit harness, it will be overwritten when you run `make run_audit_harness`, so you should back it up beforehand.
- If at any point the audit harness crashes, it is possible that the `audit.conf` file for the crashed audit test will not be cleaned up properly, so make sure to manually look for and remove it if it persists post-crash.

To run the compliance tests, follow the instructions below:

1. Make sure that you have populated `results/` with `make update_results`. You should have already done this if you are following the Submission Guide in order for the first time, but if not, see the previous section.
    1. **You must also make sure you have not yet truncated the accuracy logs before proceeding.** If you don't know what this means, that's good: you probably haven't done this yet. This step is described later. If you attempt to proceed after the accuracy logs have already been truncated, any following steps will most likely crash when you attempt to run commands.
2. Run the audit tests using the `run_audit_harness` make target, using the*same*`RUN_ARGS` you used in the 'Result Logs' section **without the test_mode=AccuracyOnly**:

```
$ make run_audit_harness RUN_ARGS="--benchmarks=... --scenarios=... --config_ver=default,high_accuracy[,triton,high_accuracy_triton]"
```
    1. **Do not** run accuracy mode for audit tests.

3. The stdout logs will show `TEST PASS` or `TEST FAIL`.

    1. In NVIDIA's submission code, it is expected that BERT audit tests will fail the first 2 parts of TEST01, since CUDA kernel selection is nondeterministic at runtime. This causes the raw output value to be slightly different, but does not affect the overall accuracy. The `run_audit_harness` make target you ran in step (2) actually automatically does the "fallback" manual path described in [TEST01 Part III](https://github.com/mlcommons/inference/tree/master/compliance/nvidia/TEST01#part-iii), so **you do not have to do this by hand**.
    2. If any compliance tests fail, even after the "autocorrection" described above for TEST01 part III, refer to the instructions in the [official compliance page](https://github.com/mlcommons/inference/tree/master/compliance/nvidia) for how to resolve each issue.
4. Once all audit tests show that they have passed, run `make update_compliance` to copy the audit test logs to `compliance/`.

### Truncating the Accuracy Logs

Since `mlperf_log_accuracy.json` files can be extremely large in size, sometimes multiple gigabytes depending on the benchmark, the rules require that the submitters truncate the `mlperf_log_accuracy.json` files using an official script, which replaces the `mlperf_log_accuracy.json` file with the first and last 4000 characters of the file, and then appends the sha256 hash of the original `mlperf_log_accuracy.json` to `accuracy.txt`. **The original, non-truncated mlperf_log_accuracy.json file should be kept in storage, in case other submitters request to see it during the submission review process.**

Follow the instructions below to truncate your logs:

1. Make sure you have completed both the "Update result logs" and "Update compliance logs" steps (see the prior 2 sections of this guide).
2. To truncate the accuracy logs, from **outside the container**, run:

```
$ make truncate_results SUBMITTER=[your company name]
```
This make target calls the [official truncation script](https://github.com/mlcommons/inference/blob/master/tools/submission/truncate_accuracy_log.py), and handles the overhead required to run the script.

3. **Important**: The truncation script will store the full logs as backup in `build/full_results`. Make sure to **copy this entire directory** over to some safe storage, such as an internal datastore, as backup, in case submission reviewers request to see them.

### Running the submission checker

The entire submission repository needs to pass the official submission checker script to be considered a valid submission. This script checks if there are missing files, errors in LoadGen logs, invalid LoadGen settings, and other common issues which do not satisfy the inference rules or the submission rules. **The output of this script must be included in** `results/submission_checker_log.txt` as proof of a valid submission.

To do this in NVIDIA's submission code, **from outside the container**, run

```
$ make check_submission SUBMITTER=[company name]
```
This command will save the output to the appropriate location. Make sure that there are no errors in the output. If the submission checker reports errors, the last line will say something like:

```
[2021-04-09 17:24:12,654 submission-checker.py:1234 ERROR] SUMMARY: submission has errors
```
Grok through the file and fix any errors that may be reported.

**Warning**: Make sure that no files and directories exist in the project root other than `closed/` and `open/`. Within these directories, make sure that no files and directories exist other than directories being the submitter's name, containing their submission code and files. If you are an NVIDIA submission partner and are encounter these errors, **make sure you unpacked the codedrop tarball in an isolated directory with no other files existing inside**.

**Note**: The [submission-checker.py](https://github.com/mlperf/inference/blob/master/tools/submission/submission-checker.py) checks if there are any ERRORs in the LoadGen detailed logs. There are a few allowed LoadGen ERRORs which seem to be caused by LoadGen issue, and are waived in the [submission-checker.py](https://github.com/mlperf/inference/blob/master/tools/submission/submission-checker.py) already. If there are other LoadGen ERRORs which you think are caused by LoadGen issue, please create an Issue in the [inference](https://github.com/mlperf/inference) repository so that the WG can discuss about it.

### Packaging your project for submission

Effective v1.0 of MLPerf Inference, there is a new "secure submission process" where submitters can submit an encrypted tarball of their submission repository, so that only the MLPerf Inference Results chair can view them prior to the deadline.

This process requires the submitter to provide the following files to the MLPerf Inference Results chair:

- An encrypted tarball of your submission repository
- A text file of the sha1 hash of the submission tarball (used as a checksum)
- The encryption password

In NVIDIA's submission, there is a script located at `scripts/pack_submission.sh`. This script is also provided in the [Official MLCommons Inference submission tools](https://github.com/mlcommons/inference/blob/master/tools/submission/pack_submission.sh). To generate the required files for an encrypted submission, follow the steps below:

1. Make sure that your OpenSSL version is at least `1.1.1` with

```
$ openssl version
OpenSSL 1.1.1  11 Sep 2018
```
If your OpenSSL version is from before 1.1.1, update your installation.

2. Open the `pack_submission.sh` script with your preferred text editor and change the `SUBMITTER` variable to your company name.
3. From **outside the container**, in the project root (i.e. where the `closed/` directory is located), run

```
$ bash scripts/pack_submission.sh --pack
```
This command will prompt to enter and then confirm an encryption password. Save this password somewhere, as you must provide it to the MLPerf Inference results chair when you do your submission. After this command finishes running, it will create the following files:

    1. `mlperf_submission_${SUBMITTER}.tar.gz` - The encrypted tarball, encrypted with AES256
    2. `mlperf_submission_${SUBMITTER}.sha1` - A text file containing the sha1 hash of the encrypted tarball
    3. `mlperf_submission_${SUBMITTER}_checker_summary.txt` - If you have run the submission checker, this file will contain the last 2 lines from `closed/NVIDIA/results/submission_checker_log.txt` as a summary

### Submit your submission

To submit, do the following actions **before** the submission deadline. **Be wary of time zone differences.** If you are afraid of possibly missing the deadline due to time zone try to submit a few hours in advance.

1. Acquire publicly readable storage accessible via web
    1. The MLPerf Inference Results chair must be able to download the files from whatever cloud storage mechanism you choose directly via `wget`, without login information.
    2. NVIDIA has tested the following web services as possible mechanisms:
        1. Google Drive - **This may not work if your tarball exceeds 100MB.** This is because Google will disable the direct download link for large files, and instead insert a "too large for Google to scan for viruses" warning.
        2. Dropbox - Make sure to make link viewable to anyone who has the link
        3. GCP Cloud Storage
    3. If you have an internal file sharing solution that satisfies the requirements, you may use that as well.
2. Upload your tarball to the cloud storage from step (1).
3. Email the following to the MLPerf Inference results chair:
    4. 1. A URL to the uploaded encrypted tarball
    2. The sha1 hash of the tarball, either as text, or attaching the generated `mlperf_submission_${SUBMITTER}.sha1`
    3. The description password
    4. Your modified scripts/pack_submission.sh to decrypt the tarball, along with instructions to run:

```
$ bash path/to/pack_submission.sh --unpack
```

    5. Optionally, `mlperf_submission_${SUBMITTER}_checker_summary.txt`

**The current MLPerf Inference Results Chair is Guenther Schmuelling** (guschmue@microsoft.com)

