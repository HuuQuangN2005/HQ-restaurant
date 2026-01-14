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
        marginBottom: 16
    },

    card: {
        borderWidth: 1,
        borderColor: "#eee",
        borderRadius: 12,
        padding: 14,
        marginBottom: 14,
        backgroundColor: "#fafafa"
    },

    date: {
        fontWeight: "600",
        fontSize: 15,
        marginBottom: 6,
        color: "#333"
    },

    status: {
        marginTop: 6,
        marginBottom: 10,
        fontStyle: "italic",
        color: "#555"
    },

    actionRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginTop: 10
    },

    editBtn: {
        flex: 1,
        marginRight: 8,
        paddingVertical: 10,
        borderRadius: 8,
        backgroundColor: "#e3f2fd",
        alignItems: "center"
    },

    editText: {
        color: "#1976d2",
        fontWeight: "600"
    },

    cancelBtn: {
        flex: 1,
        marginLeft: 8,
        paddingVertical: 10,
        borderRadius: 8,
        backgroundColor: "#ffe5e5",
        alignItems: "center"
    },

    cancelText: {
        color: "#d32f2f",
        fontWeight: "600"
    },

    emptyText: {
        textAlign: "center",
        marginTop: 40,
        color: "#888"
    },

    center: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center"
    }
});
