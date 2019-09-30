# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from cirq.contrib.quirk.cells.testing import assert_url_to_circuit_returns
from cirq.contrib.quirk.url_to_circuit import quirk_url_to_circuit


def test_arithmetic_comparison_gates():
    with pytest.raises(ValueError, match='Missing input'):
        _ = quirk_url_to_circuit('https://algassert.com/quirk#circuit={"cols":'
                                 '[["^A<B"]]}')
    assert_url_to_circuit_returns('{"cols":[["^A<B","inputA2",1,"inputB2"]]}',
                                  diagram="""
0: ───Quirk(^A<B)───
      │
1: ───A0────────────
      │
2: ───A1────────────
      │
3: ───B0────────────
      │
4: ───B1────────────
        """,
                                  maps={
                                      0b_0_00_10: 0b_1_00_10,
                                      0b_1_00_10: 0b_0_00_10,
                                      0b_0_11_10: 0b_0_11_10,
                                      0b_0_10_10: 0b_0_10_10,
                                      0b_0_01_10: 0b_1_01_10,
                                  })

    assert_url_to_circuit_returns('{"cols":[["^A>B","inputA2",1,"inputB2"]]}',
                                  maps={
                                      0b_0_11_10: 0b_1_11_10,
                                      0b_0_10_10: 0b_0_10_10,
                                      0b_0_01_10: 0b_0_01_10,
                                  })

    assert_url_to_circuit_returns('{"cols":[["^A>=B","inputA2",1,"inputB2"]]}',
                                  maps={
                                      0b_0_11_10: 0b_1_11_10,
                                      0b_0_10_10: 0b_1_10_10,
                                      0b_0_01_10: 0b_0_01_10,
                                  })

    assert_url_to_circuit_returns('{"cols":[["^A<=B","inputA2",1,"inputB2"]]}',
                                  maps={
                                      0b_0_11_10: 0b_0_11_10,
                                      0b_0_10_10: 0b_1_10_10,
                                      0b_0_01_10: 0b_1_01_10,
                                  })

    assert_url_to_circuit_returns('{"cols":[["^A=B","inputA2",1,"inputB2"]]}',
                                  maps={
                                      0b_0_11_10: 0b_0_11_10,
                                      0b_0_10_10: 0b_1_10_10,
                                      0b_0_01_10: 0b_0_01_10,
                                  })

    assert_url_to_circuit_returns('{"cols":[["^A!=B","inputA2",1,"inputB2"]]}',
                                  maps={
                                      0b_0_11_10: 0b_1_11_10,
                                      0b_0_10_10: 0b_0_10_10,
                                      0b_0_01_10: 0b_1_01_10,
                                  })


def test_arithmetic_unlisted_misc_gates():
    assert_url_to_circuit_returns('{"cols":[["^=A3",1,1,"inputA2"]]}',
                                  maps={
                                      0b_000_00: 0b_000_00,
                                      0b_000_01: 0b_001_01,
                                      0b_000_10: 0b_010_10,
                                      0b_111_11: 0b_100_11,
                                  })

    assert_url_to_circuit_returns('{"cols":[["^=A2",1,"inputA3"]]}',
                                  maps={
                                      0b_00_000: 0b_00_000,
                                      0b_00_001: 0b_01_001,
                                      0b_00_010: 0b_10_010,
                                      0b_00_100: 0b_00_100,
                                      0b_11_111: 0b_00_111,
                                  })

    assert_url_to_circuit_returns('{"cols":[[{"id":"setA","arg":5}],["^=A4"]]}',
                                  maps={
                                      0b_0000: 0b_0101,
                                      0b_1111: 0b_1010,
                                  })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":11}],["+cntA4"]]}',
        maps={
            0b_0000: 0b_0011,
            0b_0001: 0b_0100,
            0b_1111: 0b_0010,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":5}],["+cntA4"]]}',
        maps={
            0b_0000: 0b_0010,
            0b_0001: 0b_0011,
            0b_1111: 0b_0001,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":7}],["-cntA4"]]}',
        maps={
            0b_0000: 0b_1101,
            0b_0001: 0b_1110,
            0b_1111: 0b_1100,
        })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":5}],["Flip<A4"]]}',
        maps={
            0b_1111: 0b_1111,
            0b_0110: 0b_0110,
            0b_0101: 0b_0101,
            0b_0100: 0b_0000,
            0b_0011: 0b_0001,
            0b_0010: 0b_0010,
            0b_0001: 0b_0011,
            0b_0000: 0b_0100,
        })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":6}],["Flip<A4"]]}',
        maps={
            0b_1111: 0b_1111,
            0b_0110: 0b_0110,
            0b_0101: 0b_0000,
            0b_0100: 0b_0001,
            0b_0011: 0b_0010,
            0b_0010: 0b_0011,
            0b_0001: 0b_0100,
            0b_0000: 0b_0101,
        })


def test_arithmetic_addition_gates():
    assert_url_to_circuit_returns('{"cols":[["inc3"]]}',
                                  diagram="""
0: ───Quirk(inc3)───
      │
1: ───#2────────────
      │
2: ───#3────────────
            """,
                                  maps={
                                      0: 1,
                                      3: 4,
                                      7: 0,
                                  })
    assert_url_to_circuit_returns('{"cols":[["dec3"]]}',
                                  maps={
                                      0: 7,
                                      3: 2,
                                      7: 6,
                                  })
    assert_url_to_circuit_returns('{"cols":[["+=A2",1,"inputA2"]]}',
                                  maps={
                                      0b_00_00: 0b_00_00,
                                      0b_01_10: 0b_11_10,
                                      0b_10_11: 0b_01_11,
                                  })
    assert_url_to_circuit_returns('{"cols":[["-=A2",1,"inputA2"]]}',
                                  maps={
                                      0b_00_00: 0b_00_00,
                                      0b_01_10: 0b_11_10,
                                      0b_10_11: 0b_11_11,
                                  })


def test_arithmetic_multiply_accumulate_gates():
    assert_url_to_circuit_returns('{"cols":[["+=AA4",1,1,1,"inputA2"]]}',
                                  maps={
                                      0b_0000_00: 0b_0000_00,
                                      0b_0100_10: 0b_1000_10,
                                      0b_1000_11: 0b_0001_11,
                                  })

    assert_url_to_circuit_returns('{"cols":[["-=AA4",1,1,1,"inputA2"]]}',
                                  maps={
                                      0b_0000_00: 0b_0000_00,
                                      0b_0100_10: 0b_0000_10,
                                      0b_1000_11: 0b_1111_11,
                                  })

    assert_url_to_circuit_returns(
        '{"cols":[["+=AB3",1,1,"inputA2",1,"inputB2"]]}',
        maps={
            0b_000_00_00: 0b_000_00_00,
            0b_000_11_10: 0b_110_11_10,
            0b_100_11_11: 0b_101_11_11,
        })

    assert_url_to_circuit_returns(
        '{"cols":[["-=AB3",1,1,"inputA2",1,"inputB2"]]}',
        maps={
            0b_000_00_00: 0b_000_00_00,
            0b_000_11_10: 0b_010_11_10,
            0b_100_11_11: 0b_011_11_11,
        })


def test_modular_arithmetic_modulus_size():
    with pytest.raises(ValueError, match='too small for modulus'):
        _ = quirk_url_to_circuit('https://algassert.com/quirk#circuit={"cols":['
                                 '[{"id":"setR","arg":17}],["incmodR4"]]}')

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":16}],["incmodR4"]]}')
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":15}],["incmodR4"]]}')

    with pytest.raises(ValueError, match='too small for modulus'):
        _ = quirk_url_to_circuit('https://algassert.com/quirk#circuit={"cols":['
                                 '["incmodR2",1,"inputR3"]]}')

    assert_url_to_circuit_returns('{"cols":[["incmodR3",1,1,"inputR3"]]}')

    assert_url_to_circuit_returns('{"cols":[["incmodR4",1,1,1,"inputR3"]]}')

    assert_url_to_circuit_returns('{"cols":[["incmodR2",1,"inputR2"]]}')


def test_arithmetic_modular_addition_gates():
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":16}],["incmodR4"]]}',
        diagram="""
0: ───Quirk(incmodR4,r=16)───
      │
1: ───#2─────────────────────
      │
2: ───#3─────────────────────
      │
3: ───#4─────────────────────
        """,
        maps={
            0: 1,
            1: 2,
            2: 3,
            3: 4,
            4: 5,
            5: 6,
            15: 0,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":5}],["incmodR4"]]}',
        maps={
            0: 1,
            1: 2,
            2: 3,
            3: 4,
            4: 0,
            5: 5,
            15: 15,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":5}],["decmodR4"]]}',
        maps={
            0: 4,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 5,
            15: 15,
        })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":5},{"id":"setA","arg":3}],["+AmodR4"]]}',
        maps={
            0: 3,
            1: 4,
            2: 0,
            3: 1,
            4: 2,
            5: 5,
            15: 15,
        })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":5},{"id":"setA","arg":3}],["-AmodR4"]]}',
        maps={
            0: 2,
            1: 3,
            2: 4,
            3: 0,
            4: 1,
            5: 5,
            15: 15,
        })


def test_arithmetic_modular_multiply_accumulate_gates():
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":5},{"id":"setA","arg":3},'
        '{"id":"setB","arg":4}],["+ABmodR4"]]}',
        maps={
            0: 2,
            1: 3,
            2: 4,
            3: 0,
            4: 1,
            5: 5,
            15: 15,
        })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setR","arg":27},{"id":"setA","arg":3},'
        '{"id":"setB","arg":5}],["-ABmodR6"]]}',
        maps={
            0: 27 - 15,
            1: 27 - 14,
            15: 0,
            16: 1,
            26: 26 - 15,
            27: 27,
            63: 63,
        })


def test_arithmetic_multiply_gates():
    assert_url_to_circuit_returns('{"cols":[[{"id":"setA","arg":3}],["*A4"]]}',
                                  maps={
                                      0: 0,
                                      1: 3,
                                      3: 9,
                                      9: 11,
                                      11: 1,
                                  })
    assert_url_to_circuit_returns('{"cols":[[{"id":"setA","arg":3}],["/A4"]]}',
                                  maps={
                                      0: 0,
                                      1: 11,
                                      3: 1,
                                      9: 3,
                                      11: 9,
                                  })

    # Irreversible multipliers have no effect.
    assert_url_to_circuit_returns('{"cols":[[{"id":"setA","arg":4}],["*A4"]]}',
                                  maps={
                                      0: 0,
                                      1: 1,
                                      3: 3,
                                  })
    assert_url_to_circuit_returns('{"cols":[[{"id":"setA","arg":4}],["/A4"]]}',
                                  maps={
                                      0: 0,
                                      1: 1,
                                      3: 3,
                                  })


def test_arithmetic_modular_multiply_gates():
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":3},{"id":"setR","arg":7}],["*AmodR4"]]}',
        maps={
            0: 0,
            1: 3,
            3: 2,
            2: 6,
            6: 4,
            4: 5,
            5: 1,
            7: 7,
            15: 15,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":3},{"id":"setR","arg":7}],["/AmodR4"]]}',
        maps={
            0: 0,
            1: 5,
            2: 3,
            3: 1,
            4: 6,
            5: 4,
            6: 2,
            7: 7,
            15: 15,
        })

    # Irreversible multipliers have no effect.
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":5},{"id":"setR","arg":15}],["*AmodR4"]]}',
        maps={
            0: 0,
            1: 1,
            3: 3,
            15: 15,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":5},{"id":"setR","arg":15}],["/AmodR4"]]}',
        maps={
            0: 0,
            1: 1,
            3: 3,
            15: 15,
        })


def test_arithmetic_modular_exponentiation_gates():
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":5},{"id":"setB","arg":3},'
        '{"id":"setR","arg":7}],["*BToAmodR4"]]}',
        maps={
            0: 0,
            1: 5,
            2: 3,
            15: 15,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":6},{"id":"setB","arg":3},'
        '{"id":"setR","arg":7}],["*BToAmodR4"]]}',
        maps={
            0: 0,
            1: 1,
            2: 2,
            15: 15,
        })

    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":5},{"id":"setB","arg":3},'
        '{"id":"setR","arg":7}],["/BToAmodR4"]]}',
        maps={
            0: 0,
            1: 3,
            2: 6,
            15: 15,
        })
    assert_url_to_circuit_returns(
        '{"cols":[[{"id":"setA","arg":6},{"id":"setB","arg":3},'
        '{"id":"setR","arg":7}],["/BToAmodR4"]]}',
        maps={
            0: 0,
            1: 1,
            2: 2,
            15: 15,
        })