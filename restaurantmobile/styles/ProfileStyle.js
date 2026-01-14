import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#f5f5f5",
        paddingTop: 10,
    },

    guestBox: {
        alignItems: "center",
        paddingVertical: 40,
        paddingHorizontal: 20,
    },

    avatarWrapper: {
        marginBottom: 15,
    },

    guestTitle: {
        fontSize: 20,
        fontWeight: "bold",
        marginBottom: 8,
    },

    guestSubtitle: {
        fontSize: 14,
        color: "#666",
        textAlign: "center",
        marginBottom: 25,
        lineHeight: 20,
    },

    loginBtn: {
        backgroundColor: "#f5a623",
        paddingVertical: 12,
        paddingHorizontal: 40,
        borderRadius: 25,
        elevation: 3,
    },

    loginText: {
        color: "#fff",
        fontWeight: "bold",
        fontSize: 16,
    },

    userBox: {
        alignItems: "center",
        paddingVertical: 30,
        borderBottomWidth: 1,
        borderBottomColor: "#eee",
        backgroundColor: "#fff",
        marginBottom: 10,
    },

    welcomeText: {
        fontSize: 20,
        fontWeight: "bold",
        marginBottom: 4,
    },

    userSubText: {
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

    menuText: {
        fontSize: 15,
        color: "#333",
    },
    logoutBtn: {
        backgroundColor: "#fff",
        marginHorizontal: 12,
        marginTop: 12,
        paddingVertical: 14,
        borderRadius: 12,
        alignItems: "center",
        borderWidth: 1,
        borderColor: "#f5a623",
    },

    logoutText: {
        color: "#f5a623",
        fontWeight: "bold",
        fontSize: 15,
    },
});
