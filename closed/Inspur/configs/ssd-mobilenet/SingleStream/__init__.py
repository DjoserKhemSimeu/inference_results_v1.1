# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
sys.path.insert(0, os.getcwd())

from code.common.constants import Benchmark, Scenario
from code.common.system_list import System, Architecture, MIGConfiguration, MIGSlice
from configs.configuration import *


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex1(BenchmarkConfiguration):
    system = System("A100-PCIe", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex1_Triton(BenchmarkConfiguration):
    system = System("A100-PCIe", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GBx1(BenchmarkConfiguration):
    system = System("A100-PCIe-80GB", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GBx1_Triton(A100_PCIe_80GBx1):
    use_triton = True


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x1(BenchmarkConfiguration):
    system = System("A100-PCIe-80GB", Architecture.Ampere, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({0: {MIGSlice(1, 10): 1}})
    system = System("A100-SXM-80GB", Architecture.Ampere, 1, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    workspace_size = 1073741824
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_Hetero(A100_SXM_80GB_MIG_1x1g10gb):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_Triton(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({0: {MIGSlice(1, 10): 1}})
    system = System("A100-SXM-80GB", Architecture.Ampere, 1, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    workspace_size = 1073741824
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_56x1g10gb(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({
        0: {MIGSlice(1, 10): 7},
        1: {MIGSlice(1, 10): 7},
        2: {MIGSlice(1, 10): 7},
        3: {MIGSlice(1, 10): 7},
        4: {MIGSlice(1, 10): 7},
        5: {MIGSlice(1, 10): 7},
        6: {MIGSlice(1, 10): 7},
        7: {MIGSlice(1, 10): 7},
    })
    system = System("A100-SXM-80GB", Architecture.Ampere, 8, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    workspace_size = 1073741824
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_56x1g10gb_Triton(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({
        0: {MIGSlice(1, 10): 7},
        1: {MIGSlice(1, 10): 7},
        2: {MIGSlice(1, 10): 7},
        3: {MIGSlice(1, 10): 7},
        4: {MIGSlice(1, 10): 7},
        5: {MIGSlice(1, 10): 7},
        6: {MIGSlice(1, 10): 7},
        7: {MIGSlice(1, 10): 7},
    })
    system = System("A100-SXM-80GB", Architecture.Ampere, 8, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    workspace_size = 1073741824
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx1(BenchmarkConfiguration):
    system = System("A100-SXM-80GB", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx1_Triton(BenchmarkConfiguration):
    system = System("A100-SXM-80GB", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GB_MIG_1x1g5gb(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({0: {MIGSlice(1, 5): 1}})
    system = System("A100-SXM4-40GB", Architecture.Ampere, 1, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    workspace_size = 1073741824
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GB_MIG_1x1g5gb_Triton(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({0: {MIGSlice(1, 5): 1}})
    system = System("A100-SXM4-40GB", Architecture.Ampere, 1, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    workspace_size = 1073741824
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GBx1(BenchmarkConfiguration):
    system = System("A100-SXM4-40GB", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GBx1_Triton(BenchmarkConfiguration):
    system = System("A100-SXM4-40GB", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    start_from_device = True
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A10x1(BenchmarkConfiguration):
    system = System("A10", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 373000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A10x1_Triton(BenchmarkConfiguration):
    system = System("A10", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 373000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_1x1g6gb(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({0: {MIGSlice(1, 6): 1}})
    system = System("A30", Architecture.Ampere, 1, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    workspace_size = 8388608
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 450280


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_1x1g6gb_Hetero(A30_MIG_1x1g6gb):
    single_stream_expected_latency_ns = 474529


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_1x1g6gb_Triton(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({0: {MIGSlice(1, 6): 1}})
    system = System("A30", Architecture.Ampere, 1, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    workspace_size = 8388608
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 532491


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_32x1g6gb(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({
        0: {MIGSlice(1, 6): 4},
        1: {MIGSlice(1, 6): 4},
        2: {MIGSlice(1, 6): 4},
        3: {MIGSlice(1, 6): 4},
        4: {MIGSlice(1, 6): 4},
        5: {MIGSlice(1, 6): 4},
        6: {MIGSlice(1, 6): 4},
        7: {MIGSlice(1, 6): 4},
    })
    system = System("A30", Architecture.Ampere, 8, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    workspace_size = 8388608
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 512501


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_32x1g6gb_Triton(BenchmarkConfiguration):
    _mig_configuration = MIGConfiguration({
        0: {MIGSlice(1, 6): 4},
        1: {MIGSlice(1, 6): 4},
        2: {MIGSlice(1, 6): 4},
        3: {MIGSlice(1, 6): 4},
        4: {MIGSlice(1, 6): 4},
        5: {MIGSlice(1, 6): 4},
        6: {MIGSlice(1, 6): 4},
        7: {MIGSlice(1, 6): 4},
    })
    system = System("A30", Architecture.Ampere, 8, mig_conf=_mig_configuration)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    workspace_size = 8388608
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 532491


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30x1(BenchmarkConfiguration):
    system = System("A30", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 340000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30x1_Triton(BenchmarkConfiguration):
    system = System("A30", Architecture.Ampere, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 340000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class AGX_Xavier(BenchmarkConfiguration):
    system = System("AGX_Xavier", Architecture.Xavier, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    use_direct_host_access = False
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 1500000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxQ)
class AGX_Xavier_MaxQ(BenchmarkConfiguration):
    system = System("AGX_Xavier", Architecture.Xavier, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    use_direct_host_access = False
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 1500000

    # power settings
    xavier_gpu_freq = 1032750000
    xavier_dla_freq = 950000000
    xavier_cpu_freq = 1190400
    xavier_emc_freq = 1600000000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class AGX_Xavier_Triton(BenchmarkConfiguration):
    system = System("AGX_Xavier", Architecture.Xavier, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    use_direct_host_access = False
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 1500000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x1(BenchmarkConfiguration):
    system = System("T4", Architecture.Turing, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 753452


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x1_Triton(BenchmarkConfiguration):
    system = System("T4", Architecture.Turing, 1)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 753452


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class Xavier_NX(BenchmarkConfiguration):
    system = System("Xavier_NX", Architecture.Xavier, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 2
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    use_direct_host_access = False
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 2000000


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxQ)
class Xavier_NX_MaxQ(BenchmarkConfiguration):
    system = System("Xavier_NX", Architecture.Xavier, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 2
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    use_direct_host_access = False
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 2000000

    # power settings
    xavier_gpu_freq = 803250000
    xavier_dla_freq = 1100800000
    xavier_cpu_freq = 1190400
    xavier_emc_freq = 1331200000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class Xavier_NX_Triton(BenchmarkConfiguration):
    system = System("Xavier_NX", Architecture.Xavier, 1, cpu_arch=CPUArch.aarch64)
    gpu_batch_size = 1
    gpu_copy_streams = 2
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "chw4"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_chw4"
    use_direct_host_access = False
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 2000000

@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex2(BenchmarkConfiguration):
    system = System("A100-PCIe", Architecture.Ampere, 2)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000

@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIex2_MaxQ(BenchmarkConfiguration):
    system = System("A100-PCIe", Architecture.Ampere, 2)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    single_stream_expected_latency_ns = 460000

@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex2_Triton(BenchmarkConfiguration):
    system = System("A100-PCIe", Architecture.Ampere, 2)
    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    input_dtype = "int8"
    map_path = "data_maps/coco/val_map.txt"
    precision = "int8"
    use_graphs = True
    input_format = "linear"
    tensor_path = "${PREPROCESSED_DATA_DIR}/coco/val2017/SSDMobileNet/int8_linear"
    scenario = Scenario.SingleStream
    benchmark = Benchmark.SSDMobileNet
    use_triton = True
    single_stream_expected_latency_ns = 460000