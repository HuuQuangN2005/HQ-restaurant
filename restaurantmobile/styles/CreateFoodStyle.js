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
        marginBottom: 20,
        textAlign: "center",
        color: "#333"
    },

    input: {
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 10,
        paddingHorizontal: 14,
        paddingVertical: 12,
        fontSize: 16,
        marginBottom: 14,
        backgroundColor: "#fafafa"
    },

    label: {
        fontSize: 16,
        fontWeight: "600",
        marginBottom: 8,
        marginTop: 10,
        color: "#333"
    },

    categoryWrap: {
        flexDirection: "row",
        flexWrap: "wrap",
        gap: 10,
        marginBottom: 16
    },

    categoryItem: {
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: "#ccc",
        backgroundColor: "#fff"
    },

    categoryActive: {
        backgroundColor: "#f5a623",
        borderColor: "#f5a623"
    },

    submitBtn: {
        backgroundColor: "#f5a623",
        paddingVertical: 14,
        borderRadius: 12,
        alignItems: "center",
        marginTop: 10,
        marginBottom: 30
    },

    submitText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "bold"
    },
    listItem: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        paddingVertical: 12,
        paddingHorizontal: 10,
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        marginBottom: 8,
        backgroundColor: "#fafafa"
    },

    listText: {
        fontSize: 15,
        color: "#333"
    },

    radio: {
        fontSize: 18,
        color: "#f5a623"
    },

    checkbox: {
        fontSize: 18,
        color: "#f5a623"
    },

    addRow: {
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 16,
        marginTop: 6
    },

    addInput: {
        flex: 1,
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        paddingHorizontal: 10,
        paddingVertical: 8,
        marginRight: 8
    },

    addBtn: {
        backgroundColor: "#f5a623",
        width: 36,
        height: 36,
        borderRadius: 18,
        alignItems: "center",
        justifyContent: "center"
    },

    imagePicker: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        paddingVertical: 10,
        borderWidth: 1,
        borderColor: "#f5a623",
        borderRadius: 8,
        backgroundColor: "#fff7e6",
        marginBottom: 12,
    },
    imagePickerText: {
        marginLeft: 8,
        color: "#f5a623",
        fontWeight: "600",
    },

    previewImage: {
        marginLeft: 20,
        width: 120,
        height: 120,
        borderRadius: 8,
        marginBottom: 12,
        resizeMode: "cover",
    },


});
