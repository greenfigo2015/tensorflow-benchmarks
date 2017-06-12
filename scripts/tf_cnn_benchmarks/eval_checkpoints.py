import argparse
import os
import subprocess
import time

def main(input_path, command):
  cnt = 0
  with open(os.path.join(input_path, "README.md"), 'r') as f:
    output = f.read()
    time_interval = int(output.split(" = ")[1].strip().rstrip(" secs"))
  accuracies = []
  while True:
    ckpt_path = ("%5d" % cnt).replace(' ', '0')
    full_ckpt_path = os.path.join(input_path, ckpt_path)
    if not os.path.exists(full_ckpt_path):
      break
    full_command = command + " --train_dir=%s 2>/dev/null" % full_ckpt_path
    output = subprocess.check_output(full_command, shell=True)
    for line in output.split('\n'):
      if "Precision" in line and "recall" in line:
        tokens = line.split()  # TODO: Nasty hack, make more robust.
        precision_at_1 = float(tokens[4])
        recall_at_5 = float(tokens[9])
        accuracies.append([(cnt + 1) * time_interval, precision_at_1, recall_at_5])
    cnt += 1

  print "Time (in secs)\tTop 1 accuracy\tTop 5 accuracy"
  for accuracy in accuracies:
    print "\t".join([str(accuracy_token) for accuracy_token in accuracy])


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description=("Backup model checkpoints periodically")
  )
  parser.add_argument('-i', "--input_path", type=str, required=True,
                      help="Path to dumped model checkpoints")
  parser.add_argument('-c', "--command", type=str, required=True,
                      help="Command to evaluate each individual checkpoint")

  cmdline_args = parser.parse_args()
  opt_dict = vars(cmdline_args)

  main(opt_dict["input_path"], opt_dict["command"])