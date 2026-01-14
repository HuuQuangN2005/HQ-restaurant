import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#f7f7f7",
        padding: 20,
    },
    
    title: {
        fontSize: 24,
        fontWeight: "bold",
        textAlign: "center",
        marginBottom: 25,
        color: "#333",
    },

    label: {
        fontSize: 14,
        marginBottom: 6,
        marginTop: 10,
        color: "#555",
    },

    input: {
        backgroundColor: "#fff",
        borderRadius: 12,
        fontSize: 16,
    },

    loginBtn: {
        marginTop: 25,
        backgroundColor: "#f5a623",
        paddingVertical: 14,
        borderRadius: 12,
        alignItems: "center",
    },

    loginText: {
        color: "#fff",
        fontWeight: "bold",
        fontSize: 16,
        letterSpacing: 0.5,
    },

    registerText: {
        textAlign: "center",
        marginTop: 20,
        color: "#555",
    },

    registerLink: {
        color: "#f5a623",
        fontWeight: "bold",
    },
    registerBtn: {
        marginTop: 20,
        borderRadius: 12,
    },
    avatar: {
        width: 120, 
        height: 120, 
        borderRadius: 60, 
        marginTop: 10, 
        alignSelf: "center"
    }
});
