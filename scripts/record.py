#!/usr/bin/python3

import utility as u
import imageDataGatherer as i

i.getCards(u.mainHandGrab())
i.getCards(u.sideHandGrab())
i.getCards(u.dealerHandGrab())
