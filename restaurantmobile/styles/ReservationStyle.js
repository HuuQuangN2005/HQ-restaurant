import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: "#fff"
    },

    title: {
        fontSize: 24,
        fontWeight: "bold",
        marginBottom: 20,
        color: "#333"
    },

    label: {
        marginBottom: 6,
        fontSize: 15,
        color: "#555"
    },

    input: {
        borderWidth: 1,
        borderColor: "#ccc",
        borderRadius: 8,
        padding: 12,
        marginBottom: 16,
        fontSize: 15
    },

    textArea: {
        height: 100,
        textAlignVertical: "top"
    },

    submitBtn: {
        backgroundColor: "#f5a623",
        padding: 14,
        borderRadius: 10,
        alignItems: "center",
        marginTop: 10
    },

    submitText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "bold"
    }
});
