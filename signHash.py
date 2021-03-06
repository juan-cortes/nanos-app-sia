#!/usr/bin/env python
"""
*******************************************************************************
*   Ledger Blue
*   (c) 2016 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
import argparse
import base64
import struct
import sys

parser = argparse.ArgumentParser()
parser.add_argument('hash', help="hex-encoded hash to sign")
parser.add_argument('--index', type=int, help="key index to derive")
args = parser.parse_args()

if args.index == None:
	args.index = 0

if len(args.hash) != 64:
	print "Hash must be 32 bytes (64 hex characters)"
	sys.exit(1)

args.hash = args.hash.decode('hex')
dongleIndex = struct.pack("<I", int(args.index))
apdu = "e0020000".decode('hex') + chr(len(dongleIndex) + len(args.hash)) + dongleIndex + args.hash

try:
	dongle = getDongle(False)
	result = dongle.exchange(bytes(apdu))
except CommException as e:
	if (e.sw == 0x6985):
		print "User refused to sign hash"
	else:
		print "Unknown exception -- Is the Sia wallet app is running?"
	sys.exit(1)
except Exception as e:
	print e, type(e)
	print "I/O error -- Is your Nano S connected?"
	sys.exit(1)

print "Signature: " + base64.standard_b64encode(result[:64])
