import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#f6f6f6",
        paddingTop: 12,
    },

    header: {
        alignItems: "center",
        marginBottom: 16,
    },

    title: {
        fontSize: 18,
        fontWeight: "bold",
        color: "#333",
    },

    subtitle: {
        marginTop: 4,
        fontSize: 14,
        color: "#777",
    },

    menu: {
        backgroundColor: "#fff",
        borderRadius: 12,
        marginHorizontal: 12,
        overflow: "hidden",
        elevation: 2,
    },

    menuItem: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        paddingHorizontal: 16,
        paddingVertical: 14,
        borderBottomWidth: 1,
        borderBottomColor: "#eee",
    },

    menuItemLast: {
        borderBottomWidth: 0,
    },

    menuText: {
        fontSize: 15,
        color: "#333",
    },

    menuIcon: {
        color: "#999",
    },
});
