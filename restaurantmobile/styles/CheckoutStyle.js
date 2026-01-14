import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        padding: 16
    },

    title: {
        fontSize: 22,
        fontWeight: "bold",
        marginBottom: 12
    },

    sectionTitle: {
        marginTop: 18,
        marginBottom: 6,
        fontSize: 15,
        fontWeight: "600"
    },

    addressItem: {
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        padding: 10,
        marginBottom: 6
    },

    addressActive: {
        borderColor: "#ff7a00",
        backgroundColor: "#fff3e0"
    },

    input: {
        borderWidth: 1,
        borderColor: "#ccc",
        borderRadius: 8,
        padding: 10,
        marginBottom: 6
    },

    item: {
        flexDirection: "row",
        justifyContent: "space-between",
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderColor: "#eee"
    },

    itemName: {
        fontSize: 16,
        fontWeight: "500"
    },

    itemPrice: {
        color: "#555"
    },

    qty: {
        fontWeight: "600"
    },

    totalRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginTop: 20
    },

    totalLabel: {
        fontSize: 18,
        fontWeight: "bold"
    },

    totalPrice: {
        fontSize: 18,
        fontWeight: "bold",
        color: "#ff7a00"
    },

    submitBtn: {
        backgroundColor: "#ff7a00",
        paddingVertical: 14,
        borderRadius: 10,
        alignItems: "center",
        marginTop: 20
    },

    submitText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "600"
    },

    center: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center"
    },
    addNewText: {
        color: "#0077cc",
        marginVertical: 8,
        fontWeight: "600"
    },
    addressBox: {
        borderWidth: 1,
        borderColor: "#eee",
        borderRadius: 10,
        padding: 12,
        marginBottom: 8
    },

    addressLabel: {
        fontWeight: "600",
        marginBottom: 6
    },

    addressRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center"
    },

    addressText: {
        flex: 1,
        marginRight: 8,
        color: "#333"
    },

    changeText: {
        color: "#0077cc",
        fontWeight: "600"
    },

    addressOption: {
        padding: 10,
        borderBottomWidth: 1,
        borderColor: "#eee"
    },

    addressWrapper: {
        position: "relative",
        zIndex: 10
    },

    addressDropdown: {
        position: "absolute",
        top: "100%",
        left: 0,
        right: 0,
        backgroundColor: "#fff",
        borderWidth: 1,
        borderColor: "#eee",
        borderRadius: 10,
        marginTop: 6,
        maxHeight: 180,
        zIndex: 20,
        elevation: 5    
    },

    qtyRow: {
        flexDirection: "row",
        alignItems: "center"
    },

    qtyBtn: {
        width: 30,
        height: 30,
        borderRadius: 6,
        backgroundColor: "#eee",
        alignItems: "center",
        justifyContent: "center"
    },

    qtyText: {
        fontSize: 18,
        fontWeight: "bold"
    },

    qtyValue: {
        marginHorizontal: 10,
        fontSize: 16,
        fontWeight: "600"
    },



});
