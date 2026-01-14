import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        padding: 16
    },

    title: {
        fontSize: 22,
        fontWeight: "700",
        color: "#222",
        marginBottom: 12
    },

    card: {
        borderWidth: 1,
        borderColor: "#eee",
        borderRadius: 12,
        padding: 14,
        marginBottom: 12,
        backgroundColor: "#fff",
        elevation: 1,
        shadowColor: "#000",
        shadowOpacity: 0.06,
        shadowRadius: 6,
        shadowOffset: { width: 0, height: 2 }
    },

    id: {
        fontWeight: "700",
        color: "#111",
        marginBottom: 8
    },

    row: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginTop: 6
    },

    actionRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginTop: 10
    },

    label: {
        color: "#666",
        fontWeight: "600"
    },

    value: {
        color: "#222"
    },

    price: {
        fontWeight: "800",
        color: "#ff7a00"
    },

    badge: {
        alignSelf: "flex-start",
        paddingVertical: 4,
        paddingHorizontal: 10,
        borderRadius: 999,
        marginTop: 8,
        marginBottom: 10
    },

    badgePaid: {
        backgroundColor: "#e8f7ee"
    },

    badgeUnpaid: {
        backgroundColor: "#ffecec"
    },

    badgeText: {
        fontWeight: "700"
    },

    badgeTextPaid: {
        color: "#1a7f37"
    },

    badgeTextUnpaid: {
        color: "#d32f2f"
    },

    payBtn: {
        marginTop: 10,
        backgroundColor: "#ff7a00",
        paddingVertical: 12,
        borderRadius: 10,
        alignItems: "center"
    },

    payText: {
        color: "#fff",
        fontWeight: "800",
        fontSize: 15,
        width: 180
    },

    cancelText: {
        color: "#d32f2f",
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

    empty: {
        textAlign: "center",
        marginTop: 40,
        color: "#888"
    },

    center: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center"
    },
    badgeCanceled: {
        backgroundColor: "#fdecea",
    },
    badgeTextCanceled: {
        color: "#d32f2f",
        fontWeight: "bold",
    },
});
