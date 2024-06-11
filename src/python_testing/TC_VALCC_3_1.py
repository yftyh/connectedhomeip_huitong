#
#    Copyright (c) 2023 Project CHIP Authors
#    All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import time

import chip.clusters as Clusters
from chip.clusters.Types import NullValue
from chip.interaction_model import InteractionModelError, Status
from matter_testing_support import MatterBaseTest, TestStep, async_test_body, default_matter_test_main
from mobly import asserts


class TC_VALCC_3_1(MatterBaseTest):
    async def read_valcc_attribute_expect_success(self, endpoint, attribute):
        cluster = Clusters.Objects.ValveConfigurationAndControl
        return await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=attribute)

    def desc_TC_VALCC_3_1(self) -> str:
        return "[TC-VALCC-3.1] Basic state functionality with DUT as Server"

    def steps_TC_VALCC_3_1(self) -> list[TestStep]:
        steps = [
            TestStep(1, "Commissioning, already done", is_commissioning=True),
            TestStep(2, "Send Open command"),
            TestStep(3, "Read TargetState attribute"),
            TestStep(4, "Read CurrentState attribute"),
            TestStep(5, "Send Close command"),
            TestStep(6, "Read TargetState attribute"),
            TestStep(7, "Read CurrentState attribute"),
        ]
        return steps

    def pics_TC_VALCC_3_1(self) -> list[str]:
        pics = [
            "VALCC.S",
        ]
        return pics

    @async_test_body
    async def test_TC_VALCC_3_1(self):

        endpoint = self.user_params.get("endpoint", 1)

        self.step(1)
        attributes = Clusters.ValveConfigurationAndControl.Attributes

        self.step(2)
        try:
            await self.send_single_cmd(cmd=Clusters.Objects.ValveConfigurationAndControl.Commands.Open(), endpoint=endpoint)
        except InteractionModelError as e:
            asserts.assert_equal(e.status, Status.Success, "Unexpected error returned")
            pass

        self.step(3)
        target_state_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.TargetState)

        asserts.assert_true(target_state_dut is not NullValue, "TargetState is null")
        asserts.assert_equal(target_state_dut, Clusters.Objects.ValveConfigurationAndControl.Enums.ValveStateEnum.kOpen,
                             "TargetState is not the expected value")

        self.step(4)
        current_state_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.CurrentState)
        asserts.assert_true(current_state_dut is not NullValue, "CurrentState is null")

        while current_state_dut is Clusters.Objects.ValveConfigurationAndControl.Enums.ValveStateEnum.kTransitioning:
            time.sleep(1)

            current_state_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.CurrentState)
            asserts.assert_true(current_state_dut is not NullValue, "CurrentState is null")

        asserts.assert_equal(current_state_dut, Clusters.Objects.ValveConfigurationAndControl.Enums.ValveStateEnum.kOpen,
                             "CurrentState is not the expected value")

        self.step(5)
        try:
            await self.send_single_cmd(cmd=Clusters.Objects.ValveConfigurationAndControl.Commands.Close(), endpoint=endpoint)
        except InteractionModelError as e:
            asserts.assert_equal(e.status, Status.Success, "Unexpected error returned")
            pass

        self.step(6)
        target_state_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.TargetState)

        asserts.assert_true(target_state_dut is not NullValue, "TargetState is null")
        asserts.assert_equal(target_state_dut, Clusters.Objects.ValveConfigurationAndControl.Enums.ValveStateEnum.kClosed,
                             "TargetState is not the expected value")

        self.step(7)
        current_state_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.CurrentState)
        asserts.assert_true(current_state_dut is not NullValue, "CurrentState is null")

        while current_state_dut is Clusters.Objects.ValveConfigurationAndControl.Enums.ValveStateEnum.kTransitioning:
            time.sleep(1)

            current_state_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.CurrentState)
            asserts.assert_true(current_state_dut is not NullValue, "CurrentState is null")

        asserts.assert_equal(current_state_dut, Clusters.Objects.ValveConfigurationAndControl.Enums.ValveStateEnum.kClosed,
                             "CurrentState is not the expected value")


if __name__ == "__main__":
    default_matter_test_main()
