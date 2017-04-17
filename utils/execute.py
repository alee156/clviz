#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
import sys
import pickle

import clarityviz as clv

import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

# def s3_push_data(bucket, remote, outDir, modifier, creds=True):
#     cmd = 'aws s3 cp --exclude "tmp/*" {} s3://{}/{}/{} --recursive --acl public-read'
#     cmd = cmd.format(outDir, bucket, remote, modifier)
#     if not creds:
#         print("Note: no credentials provided, may fail to push big files.")
#         cmd += ' --no-sign-request'
#     mgu.execute_cmd(cmd)

def get_args():
    parser = argparse.ArgumentParser(description="This is the script to run the pipeline.")

    parser.add_argument("--token", type=str, required=True, help="The token of the brain of interest.")
    parser.add_argument("--resolution", type=int, help="The desired resolution of the brain.", default=5)

    args = parser.parse_args()
    check_args(args)

    return args

def check_args(args):
    # if args.token.lower() == "train":
    #     if args.algorithm is None:
    #         raise Exception("--algorithm should be specified in mode \"train\"")
    # else:
    #     if args.predictions_file is None:
    #         raise Exception("--prediction-file should be specified in mode \"test\"")
    #     if not os.path.exists(args.model_file):
    #         raise Exception("model file specified by --model-file does not exist.")
    if not (args.resolution >= 0 and args.resolution <= 5):
        raise Exception("--resolution should be an integer between 0 and 5 inclusive.")

def main():
    global args
    args = get_args()

    clv.analysis.run_pipeline(args.token, 'userToken.pem', args.resolution)

    zipf = zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('output/', zipf)
    zipf.close()

if __name__ == "__main__":
    main()
