import java.io.ByteArrayOutputStream;
import java.util.Arrays;

public class Ascon {

    private static final long[] ROUND_CONSTANTS_12 = {
        0x00000000000000f0L, 0x00000000000000e1L, 0x00000000000000d2L,
        0x00000000000000c3L, 0x00000000000000b4L, 0x00000000000000a5L,
        0x0000000000000096L, 0x0000000000000087L, 0x0000000000000078L,
        0x0000000000000069L, 0x000000000000005aL, 0x000000000000004bL
    };

    private static final long[] ROUND_CONSTANTS_6 = {
        0x0000000000000096L, 0x0000000000000087L, 0x0000000000000078L,
        0x0000000000000069L, 0x000000000000005aL, 0x000000000000004bL
    };

    private static byte[] pad(byte[] data) {
        int paddingLen = 8 - (data.length % 8);
        byte[] padded = Arrays.copyOf(data, data.length + paddingLen);
        padded[data.length] = (byte) 0x80;
        // Remaining bytes are already 0x00 due to Arrays.copyOf initialization
        return padded;
    }

    private static void asconPermutation(long[] S, int rounds) {
        long[] roundConstants = (rounds == 12) ? ROUND_CONSTANTS_12 : ROUND_CONSTANTS_6;

        for (int i = 0; i < rounds; i++) {
            // Round constant injection
            S[2] ^= roundConstants[i];
            
            // Substitution layer
            S[0] ^= S[4]; S[4] ^= S[3]; S[2] ^= S[1];
            long T0 = ~S[0];
            long T1 = ~S[1];
            long T2 = ~S[2];
            long T3 = ~S[3];
            long T4 = ~S[4];
            T0 &= S[1]; T1 &= S[2]; T2 &= S[3]; T3 &= S[4]; T4 &= S[0];
            S[0] ^= T1; S[1] ^= T2; S[2] ^= T3; S[3] ^= T4; S[4] ^= T0;
            S[1] ^= S[0]; S[0] ^= S[4]; S[3] ^= S[2]; S[2] = ~S[2];
            
            // Linear diffusion layer (Java's rotateRight naturally maps to Python's R)
            S[0] ^= Long.rotateRight(S[0], 19) ^ Long.rotateRight(S[0], 28);
            S[1] ^= Long.rotateRight(S[1], 61) ^ Long.rotateRight(S[1], 39);
            S[2] ^= Long.rotateRight(S[2], 1)  ^ Long.rotateRight(S[2], 6);
            S[3] ^= Long.rotateRight(S[3], 10) ^ Long.rotateRight(S[3], 17);
            S[4] ^= Long.rotateRight(S[4], 7)  ^ Long.rotateRight(S[4], 41);
        }
    }

    private static byte[] toBytes(long n) {
        byte[] b = new byte[8];
        for (int i = 7; i >= 0; i--) {
            b[i] = (byte) (n & 0xFF);
            n >>= 8;
        }
        return b;
    }

    private static long fromBytes(byte[] b, int offset) {
        long result = 0;
        for (int i = 0; i < 8; i++) {
            result <<= 8;
            result |= (b[offset + i] & 0xFFL);
        }
        return result;
    }

    private static long[] initialize(byte[] key, byte[] nonce) {
        if (key.length != 16 || nonce.length != 16) {
            throw new IllegalArgumentException("Key and nonce must be 16 bytes.");
        }

        long K1 = fromBytes(key, 0);
        long K2 = fromBytes(key, 8);
        long N1 = fromBytes(nonce, 0);
        long N2 = fromBytes(nonce, 8);

        long[] S = {0x80400c0600000000L, K1, K2, N1, N2};
        
        asconPermutation(S, 12);
        S[3] ^= K1;
        S[4] ^= K2;
        return S;
    }

    private static void processAssociatedData(long[] S, byte[] ad) {
        byte[] padded = pad(ad);
        for (int i = 0; i < padded.length; i += 8) {
            long blockAsInt = fromBytes(padded, i);
            S[0] ^= blockAsInt;
            asconPermutation(S, 6);
        }
        S[4] ^= 1;
    }

    private static byte[] processData(long[] S, byte[] data, String operation) {
        int originalLen = data.length;
        byte[] padded = pad(data);
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        long decryptedBlock = 0;

        for (int i = 0; i < padded.length; i += 8) {
            long blockAsInt = fromBytes(padded, i);
            
            if (operation.equals("encrypt")) {
                S[0] ^= blockAsInt;
                output.write(toBytes(S[0]), 0, 8);
            } else { // decrypt
                decryptedBlock = S[0] ^ blockAsInt;
                output.write(toBytes(decryptedBlock), 0, 8);
                S[0] ^= decryptedBlock;
            }
            
            if (i != padded.length - 8) {
                asconPermutation(S, 6);
            } else if (operation.equals("decrypt")) {
                // Handle last block in decryption differently
                S[0] ^= decryptedBlock;
                S[0] ^= 0x8000000000000000L;
            }
        }
        
        return Arrays.copyOf(output.toByteArray(), originalLen);
    }

    private static byte[] finalizeState(long[] S, byte[] key) {
        long[] S_final = S.clone();
        
        long K1 = fromBytes(key, 0);
        long K2 = fromBytes(key, 8);
        S_final[1] ^= K1;
        S_final[2] ^= K2;
        
        asconPermutation(S_final, 12);
        
        S_final[3] ^= K1;
        S_final[4] ^= K2;
        
        byte[] tag = new byte[16];
        System.arraycopy(toBytes(S_final[3]), 0, tag, 0, 8);
        System.arraycopy(toBytes(S_final[4]), 0, tag, 8, 8);
        return tag;
    }

    public static class CiphertextWithTag {
        public final byte[] ciphertext;
        public final byte[] tag;

        public CiphertextWithTag(byte[] ciphertext, byte[] tag) {
            this.ciphertext = ciphertext;
            this.tag = tag;
        }
    }

    public static CiphertextWithTag encrypt(byte[] key, byte[] nonce, byte[] plaintext, byte[] ad) {
        long[] S = initialize(key, nonce);
        if (ad.length == 0) {
            S[4] ^= 1;
        } else {
            processAssociatedData(S, ad);
        }
        byte[] ciphertext = processData(S, plaintext, "encrypt");
        byte[] tag = finalizeState(S, key);

        return new CiphertextWithTag(ciphertext, tag);
    }

    public static byte[] decrypt(byte[] key, byte[] nonce, byte[] ciphertext, byte[] tag, byte[] ad) {
        long[] S = initialize(key, nonce);
        if (ad.length == 0) {
            S[4] ^= 1;
        } else {
            processAssociatedData(S, ad);
        }
        byte[] plaintext = processData(S, ciphertext, "decrypt");
        byte[] computedTag = finalizeState(S, key);
        
        if (!Arrays.equals(tag, computedTag)) {
            throw new IllegalArgumentException("Invalid authentication tag");
        }

        return plaintext;
    }

    // Utility methods for Hex encode/decode to match Python's bytes.fromhex() and .hex()
    private static byte[] fromHex(String hex) {
        byte[] data = new byte[hex.length() / 2];
        for (int i = 0; i < data.length; i++) {
            data[i] = (byte) Integer.parseInt(hex.substring(i * 2, i * 2 + 2), 16);
        }
        return data;
    }

    private static String toHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    public static void test() {
        byte[] key = fromHex("1".repeat(32));
        byte[] nonce = fromHex("0".repeat(32));
        //byte[] plaintext = fromHex("1".repeat(64));
        //byte[] plaintext = fromHex("0".repeat(64));
        //byte[] plaintext = fromHex("77656C636F6D65746F74686563756D7A6F6E6500000000000000000000000000");
        byte[] plaintext = fromHex("7365676773000000000000000000000000000000000000000000000000000000");
        byte[] associatedData = fromHex("1".repeat(32));
        
        CiphertextWithTag result = encrypt(key, nonce, plaintext, associatedData);
        
        System.out.println("Initial plaintext: " + toHex(plaintext));
        System.out.println("Key: " + toHex(key));
        System.out.println("Nonce: " + toHex(nonce));
        System.out.println("Associated data: " + toHex(associatedData));
        System.out.println("Ciphertext: " + toHex(result.ciphertext));
        System.out.println("Tag: " + toHex(result.tag));
        
        try {
            byte[] decrypted = decrypt(key, nonce, result.ciphertext, result.tag, associatedData);
            if (Arrays.equals(decrypted, plaintext)) {
                System.out.println("Test passed.");
            } else {
                System.out.println("Test failed. Decrypted plaintext does not match.");
            }
        } catch (IllegalArgumentException e) {
            System.out.println("Test failed. " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        test();
    }
}
