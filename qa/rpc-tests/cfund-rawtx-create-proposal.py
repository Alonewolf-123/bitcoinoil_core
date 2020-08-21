#!/usr/bin/env python3
# Copyright (c) 2018 The Bitcoinoil Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import BitcoinOilTestFramework
from test_framework.cfund_util import *

import time

class CommunityFundRawTXCreateProposalTest(BitcoinOilTestFramework):
    """Tests the state transition of proposals of the Community fund."""

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 1


        self.goodDescription = "these are not the BTCO Droids you are looking for"
        self.goodDuration = 360000
        self.goodAmount = 100
        self.goodPropHash = ""
        self.goodAddress = ""

    def setup_network(self, split=False):
        self.all_desc_text_options()

        self.nodes = self.setup_nodes()
        self.is_network_split = split

    def run_test(self):
        self.nodes[0].staking(False)
        activate_cfund(self.nodes[0])

        # creates a good proposal and sets things we use later
        self.test_happy_path()

        # test incorrect amounts
        self.test_invalid_proposal(self.goodAddress, -100, self.goodDuration, "I should not work")
        self.test_invalid_proposal(self.goodAddress, -1, self.goodDuration, "I should not work")
        self.test_invalid_proposal(self.goodAddress, 0, self.goodDuration, "I should not work")
        self.test_invalid_proposal(self.goodAddress, "", self.goodDuration, "I should not work")


        # test incorrect duration
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, 0, "I should not work")
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, -13838, "I should not work")
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, True, "I should not work")
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, False, "I should not work")
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, "dsf", "I should not work")
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, "36000", "I should not work")
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, "", "I should not work")

        # test invalid address
        self.test_invalid_proposal("", self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal("a", self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal("1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY", self.goodAmount, self.goodDuration, "I should not work") # bitcoin address
        self.test_invalid_proposal("NPyEJsv82GaguVsY3Ur4pu4WwnFCsYQ94g", self.goodAmount, self.goodDuration, "I should not work") # nav address we don't own
        self.test_invalid_proposal(False, self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal(True, self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal(8888, self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal(-8888, self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal(0, self.goodAmount, self.goodDuration, "I should not work")
        self.test_invalid_proposal(1, self.goodAmount, self.goodDuration, "I should not work")

        # test invalid descriptions
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, self.descTxtToLong)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, 800)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, True)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, False)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, -100)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, 0)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, 1)
        self.test_invalid_proposal(self.goodAddress, self.goodAmount, self.goodDuration, -1)

        self.test_valid_description(self.descTxtWhiteSpace, 2)
        self.test_valid_description(self.descTxtMaxLength, 3)
        self.test_valid_description(self.descTxtAllCharsAtoB, 4)
        self.test_valid_description(self.descTxtAllCharsCtoE, 5)
        self.test_valid_description(self.descTxtAllCharsCtoE, 6)
        self.test_valid_description(self.descTxtAllCharsFtoG, 7)
        self.test_valid_description(self.descTxtAllCharsHtoK, 8)
        self.test_valid_description(self.descTxtAllCharsLtoN, 9)
        self.test_valid_description(self.descTxtAllCharsOtoP, 10)
        self.test_valid_description(self.descTxtAllCharsQtoS, 11)
        self.test_valid_description(self.descTxtAllCharsTtoU, 12)
        self.test_valid_description(self.descTxtAllCharsVtoZ, 13)
        self.test_valid_description(self.descTxtAllCharsArrows1, 14)
        self.test_valid_description(self.descTxtAllCharsArrows2, 15)
        self.test_valid_description(self.descTxtAllCharsArrows3, 16)
        self.test_valid_description(self.descTxtAllCharsClassic1, 17)
        self.test_valid_description(self.descTxtAllCharsClassic2, 18)
        self.test_valid_description(self.descTxtAllCharsCurrency, 19)
        self.test_valid_description(self.descTxtAllCharsShapes1, 20)
        self.test_valid_description(self.descTxtAllCharsShapes2, 21)
        self.test_valid_description(self.descTxtAllCharsShapes3, 22)
        self.test_valid_description(self.descTxtAllCharsShapes4, 23)
        self.test_valid_description(self.descTxtAllCharsShapes4, 24)
        self.test_valid_description(self.descTxtAllCharsMath1, 25)
        self.test_valid_description(self.descTxtAllCharsMath2, 26)
        self.test_valid_description(self.descTxtAllCharsMath3, 27)
        self.test_valid_description(self.descTxtAllCharsMath4, 28)
        self.test_valid_description(self.descTxtAllCharsNumerals1, 29)
        self.test_valid_description(self.descTxtAllCharsNumerals2, 30)
        self.test_valid_description(self.descTxtAllCharsPunch1, 31)
        self.test_valid_description(self.descTxtAllCharsPunch2, 32)
        self.test_valid_description(self.descTxtAllCharsSymbol1, 33)
        self.test_valid_description(self.descTxtAllCharsSymbol2, 34)
        self.test_valid_description(self.descTxtAllCharsSymbol3, 35)

        # i = 4
        # for char in self.descTxtAllCharsAtoE:
        #     i = i + 1
        #     self.test_desc_should_succeed(char, i)

    def test_invalid_proposal(self, address, amount, duration, description):

        # Create new payment request for more than the amount
        proposal = ""
        callSucceed = False
        try:
            proposal = self.send_raw_proposalrequest(address, amount, duration, description)
            #print(proposal)
            callSucceed = True
        except :
            pass

        assert(proposal == "")
        assert(callSucceed is False)

        #check a gen - should still only have the last good prop
        blocks = slow_gen(self.nodes[0], 1)
        proposal_list = self.nodes[0].listproposals()

        #should still only have 1 proposal from the good test run
        assert(len(proposal_list) == 1)
        self.check_good_proposal(proposal_list[0])


    def test_valid_description(self, descriptionTxt, proposal_list_len):

        duration = 360000
        amount = 100

        # Create new payment request for more than the amount
        propHash = ""
        callSucceed = True

        #print("Test Description: -------------------------")
        #print(descriptionTxt)
        try:
            propHash = self.send_raw_proposalrequest(self.goodAddress, self.goodAmount, self.goodDuration, descriptionTxt)
            #print(propHash)
        except Exception as e:
            print(e)
            callSucceed = False

        assert(propHash != "")
        assert (callSucceed is True)

        # check a gen - should still only have the last good prop
        blocks = slow_gen(self.nodes[0], 1)
        proposal_list = self.nodes[0].listproposals()

        # should still only have the correct amount of proposals from the other runs
        assert(len(proposal_list) == proposal_list_len)

        # find the proposal we just made and test the description
        proposal_found = False
        for proposal in proposal_list:
            if proposal['hash'] == propHash:
                proposal_found = True
                assert(proposal['description'] == descriptionTxt)

        assert(proposal_found)



    # Test everything the way it should be
    def test_happy_path(self):

        self.goodAddress = self.nodes[0].getnewaddress()

        self.goodPropHash = self.send_raw_proposalrequest(self.goodAddress, self.goodAmount, self.goodDuration, self.goodDescription)

        blocks = slow_gen(self.nodes[0], 1)
        proposal_list = self.nodes[0].listproposals()

        # Should only have 1 proposal
        assert(len(proposal_list) == 1)

        # The proposal should have all the same required fields
        assert (proposal_list[0]['blockHash'] == blocks[0])
        self.check_good_proposal(proposal_list[0])

    def check_good_proposal(self, proposal):

        assert (proposal['votingCycle'] == 0)
        assert (proposal['version'] == 2)
        assert (proposal['paymentAddress'] == self.goodAddress)
        assert (proposal['proposalDuration'] == self.goodDuration)
        assert (proposal['description'] == self.goodDescription)
        assert (proposal['votesYes'] == 0)
        assert (proposal['votesNo'] == 0)
        assert (proposal['status'] == 'pending')
        assert (proposal['state'] == 0)
        assert (proposal['hash'] == self.goodPropHash)
        assert (float(proposal['requestedAmount']) == float(self.goodAmount))
        assert (float(proposal['notPaidYet']) == float(self.goodAmount))
        assert (float(proposal['userPaidFee']) == float(1))


    def send_raw_proposalrequest(self, address, amount, time, description):

        amount = amount * 100000000

        # Create a raw proposal tx
        raw_proposal_tx = self.nodes[0].createrawtransaction(
            [],
            {"6ac1": 1},
            json.dumps({"v": 2, "n": amount, "a": address,  "d": time, "s": description})
        )

        # Modify version
        raw_proposal_tx = "04" + raw_proposal_tx[2:]

        # Fund raw transaction
        raw_proposal_tx = self.nodes[0].fundrawtransaction(raw_proposal_tx)['hex']

        # Sign raw transaction
        raw_proposal_tx = self.nodes[0].signrawtransaction(raw_proposal_tx)['hex']

        # Send raw transaction
        return self.nodes[0].sendrawtransaction(raw_proposal_tx)


    def all_desc_text_options(self):
        self.descTxtToLong = "LOOOOONNNNNGGGG, Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque semper justo ac neque mollis, a cursus nisl placerat. Aliquam ipsum quam, congue vitae vulputate id, ullamcorper vel libero. Phasellus et tristique justo. Curabitur eu porta magna, vitae auctor libero. Fusce tellus ipsum, aliquet nec consequat ut, dictum eget libero. Maecenas eu velit quam. Nunc ac libero in purus vestibulum feugiat quis nec urna. Donec faucibus consequat dignissim. Donec ornare turpis nec lobortis vestibulum. Vivamus lobortis vel massa ac ultrices. Ut vel eros in elit vehicula luctus vel vitae justo. Praesent quis semper nisi. Vivamus viverra blandit ex. Sed nec fringilla quam. Nulla condimentum rhoncus erat sit amet vulputate. Phasellus viverra sagittis consequat. Sed dapibus augue ac enim dignissim, at consequat arcu ornare. Vestibulum facilisis pretium aliquet. asdfjasdlkfjhadsfkjhasdkjhakjdhfaskjdakjsdhf  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.descTxtMaxLength ="IM LOOOOONNNNNGGGG, Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque semper justo ac neque mollis, a cursus nisl placerat. Aliquam ipsum quam, congue vitae vulputate id, ullamcorper vel libero. Phasellus et tristique justo. Curabitur eu porta magna, vitae auctor libero. Fusce tellus ipsum, aliquet nec consequat ut, dictum eget libero. Maecenas eu velit quam. Nunc ac libero in purus vestibulum feugiat quis nec urna. Donec faucibus consequat dignissim. Donec ornare turpis nec lobortis vestibulum. Vivamus lobortis vel massa ac ultrices. Ut vel eros in elit vehicula luctus vel vitae justo. Praesent quis semper nisi. Vivamus viverra blandit ex. Sed nec fringilla quam. Nulla condimentum rhoncus erat sit amet vulputate. Phasellus viverra sagittis consequat. Sed dapibus augue ac enim dignissim, at consequat arcu ornare. Vestibulum facilisis pretium aliquet. xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxabc"

        self.descTxtAllCharsAtoB = "??? ??? ??? A a ??? ??? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ??? ??? ??? B b ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ???"
        self.descTxtAllCharsCtoE = "??? ??? ??? C c ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? D d ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? E e ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??"
        self.descTxtAllCharsFtoG = "??? ??? ??? F f ??? ??? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? G g ?? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ?? ?? ??"
        self.descTxtAllCharsHtoK = "??? ??? ??? H h ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? I i ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? J j ?? ?? ?? ?? ?? ??? ?? ??? ??? ??? K k ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ?? ?? ??? ??? ?? "
        self.descTxtAllCharsLtoN = "??? ??? ??? L l ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ?? ??? ??? ??? ?? ?? ?? ??? ?? ??? ??? ??? ??? ?? ?? ?? ?? ??? ??? ??? ??? ??? M m ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ??? ??? ??? ??? N n ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ???"
        self.descTxtAllCharsOtoP = "??? ??? ??? O o ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? P p ??? ??? ??? ??? ?? ?? ??? ??? ?? "
        self.descTxtAllCharsQtoS = "??? ??? ??? ??? ??? Q q ?? ?? ??? ??? ?? ??? ??? ??? R r ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? S s ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ?? ?? ?? ?? ??? ?? ??? ??? ??? ???"
        self.descTxtAllCharsTtoU = "??? ??? ??? T t ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ?? ?? ?? ?? ??? ?? ??? ??? ??? ??? ??? U u ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??"
        self.descTxtAllCharsVtoZ = "??? ??? ??? V v ??? ??? ??? ??? ?? ??? ??? ??? ??? ??? ??? ??? ??? W w ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ??? ??? ?? ?? ??? ??? ??? ??? X x ??? ??? ??? ??? ??? ?? ??? ??? ??? y Y ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? Z z ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ??? ??? ?? ?? ?? ??? ???"
        self.descTxtAllCharsArrows1 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsArrows2 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsArrows3 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsClassic1 = "??? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ??? $ ?? ?? ?? @ ?? ?? ?? ??? ?? ?? ?? ?? ??? ??? ?? ??? ??? ?? ~ ??? ?? ?? ?? ?? ?? ?? ??? ??? ??? | ??? \ [ ] { } ??? ??? ??? ?? ??? ??? ??? ??? ??? ??? ??? ?? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsClassic2 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??"
        self.descTxtAllCharsCurrency = "??? ??? ??? ??? ?? ??? ??? ??? ??? ??? ?? ??? ??? ?? ??? ??? ??? ??? ??? ??? $ ??? ??? ??? ?? ??? ??? ?? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsShapes1 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? "
        self.descTxtAllCharsShapes2 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsShapes3 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? _ ??? ??? ??? ??? ??? ??? ??? ??? - ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsShapes4 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsMath1 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsMath2 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? "
        self.descTxtAllCharsMath3 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsMath4 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsNumerals1 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsNumerals2 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ?? ??? ?? ??? ?? ??? ??? ??? ??? ??? ??? ??? ??? ?? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsPunch1 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ?? ?? ??? ??? ???  < > @ ?? ??? ?? ??? ??? : ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ; ??? ??? ??? ??? ??? - ??? ??? ??? ??? _ ~ ??? ??? ??? ??? ??? ?? / \ ??? \ ??? | ??? ?? ??? ??? "
        self.descTxtAllCharsPunch2 = "??? ??? ?? ??? ??? ?? ??? ??? % ??? ??? & ??? ?? ?? + ?? = ??? ??? ??? ??? ??? ??? ??? ??? ??? * ??? ??? ??? ??? ??? ??? ! ??? ?? ? ?? ??? ??? ??? ??? ??? ??? ?? ?? ?? ?? ?? ?? ?? ??? ??? ??? ??? ??? ??? ??? ?? ??? ??? ??? ??? ??? ??? ??? ??? ( ) [ ] { } ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? '"
        self.descTxtAllCharsSymbol1 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsSymbol2 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"
        self.descTxtAllCharsSymbol3 = "??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???"


        self.descTxtWhiteSpace = '''I 
Have
Enters



And      white     space '''

if __name__ == '__main__':
    CommunityFundRawTXCreateProposalTest().main()
