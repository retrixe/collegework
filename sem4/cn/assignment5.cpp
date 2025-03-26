#include <iostream>

using namespace std;

string ipAddressAsString(unsigned int ipAddress) {
    string ipAddressString;
    ipAddressString.append(to_string(ipAddress >> 24 & 0xFF));
    ipAddressString.append(".");
    ipAddressString.append(to_string(ipAddress >> 16 & 0xFF));
    ipAddressString.append(".");
    ipAddressString.append(to_string(ipAddress >> 8 & 0xFF));
    ipAddressString.append(".");
    ipAddressString.append(to_string(ipAddress & 0xFF));
    return ipAddressString;
}

int main() {
    int ipAddress[4];
    int subnetSuffix;
    char ch;
    cout << "Enter IP address with subnet in CIDR notation: ";
    cin >> ipAddress[0] >> ch >> ipAddress[1] >> ch >> ipAddress[2] >> ch >> ipAddress[3] >> ch >> subnetSuffix;
    unsigned int ipInt = (ipAddress[0] << 24) | (ipAddress[1] << 16) | (ipAddress[2] << 8) | ipAddress[3];

    cout << "IP address: " << ipAddressAsString(ipInt) << endl;
    cout << "Subnet suffix: " << subnetSuffix << endl;

    // Display class of IP address
    if (ipAddress[0] >= 1 && ipAddress[0] <= 126) {
        cout << "Class A (Default subnet mask: 255.0.0.0)" << endl;
    } else if (ipAddress[0] >= 128 && ipAddress[0] <= 191) {
        cout << "Class B (Default subnet mask: 255.255.0.0)" << endl;
    } else if (ipAddress[0] >= 192 && ipAddress[0] <= 223) {
        cout << "Class C (Default subnet mask: 255.255.255.0)" << endl;
    } else if (ipAddress[0] >= 224 && ipAddress[0] <= 239) {
        cout << "Class D (Multicast)" << endl;
    } else if (ipAddress[0] >= 240 && ipAddress[0] <= 255) {
        cout << "Class E (Reserved)" << endl;
    } else {
        cout << "Invalid IP Address" << endl;
    }

    unsigned int subnetMask = 0xFFFFFFFF << (32 - subnetSuffix);
    cout << "Subnet Mask: " << ipAddressAsString(subnetMask) << endl;


    unsigned int networkAddress = ipInt & subnetMask; // Keep only network bits
    unsigned int broadcastAddress = ipInt | ~subnetMask; // Set to 1 all host bits
    unsigned int startAddress = networkAddress + 1;
    unsigned int endAddress = broadcastAddress - 1;

    cout << "Network Address: " << ipAddressAsString(networkAddress) << endl;
    cout << "Broadcast Address: " << ipAddressAsString(broadcastAddress) << endl;

    cout << "IP Range: " << ipAddressAsString(startAddress) << " - "  << ipAddressAsString(endAddress) << endl;
}
