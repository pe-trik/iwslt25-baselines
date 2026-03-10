import matplotlib.pyplot as plt

def load_file(file):
    with open(file, 'r') as f:
        line = f.readlines()[-1].split()
    return float(line[1]), float(line[0])

for step in range(1, 11):
    step = step / 10
    xs, ys = [], []
    for policy in range(1, 5):
        file = f"final/segment-length_24_step-length_{step}_translation-la-policy_{policy}_transcript-context_30_translation-max-input-length-soft_0/scores.resegmented.tsv"
        try:
            x, y = load_file(file)
            xs.append(x)
            ys.append(y)
        except:
            print(f"step: {step}, policy: {policy} not found")
            pass
    plt.plot(xs, ys, label=f"step={step}")
plt.legend()
plt.xlabel("Latency (ms)")
plt.ylabel("BLEU")
plt.title("Latency-Quality Tradeoff")
plt.savefig("final/tradeoff.png")