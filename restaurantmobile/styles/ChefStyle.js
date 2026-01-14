import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
    },

    header: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        padding: 16,
    },

    headerTitle: {
        fontSize: 22,
        fontWeight: "bold",
    },

    foodItem: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#fff",
        marginHorizontal: 12,
        marginVertical: 6,
        borderRadius: 12,
        padding: 10,
        elevation: 2,
    },

    foodImage: {
        width: 70,
        height: 70,
        borderRadius: 8,
        marginRight: 12,
        backgroundColor: "#eee",
    },

    foodInfo: {
        marginLeft: 12,
        flex: 1,
    },

    foodName: {
        fontSize: 16,
        fontWeight: "600",
    },

    foodPrice: {
        color: "#e53935",
        marginTop: 4,
        fontWeight: "500",
    },

    actionBtn: {
        marginLeft: 10,
    },

    emptyText: {
        textAlign: "center",
        marginTop: 40,
        color: "#999",
    },
    foodMain: {
        flexDirection: "row",
        flex: 1,
        alignItems: "center",
    },
});
