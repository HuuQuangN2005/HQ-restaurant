import { StyleSheet, Dimensions } from "react-native";

const width = Dimensions.get("window").width;

export default StyleSheet.create({
    container: {
        flexDirection: "row",
        padding: 16,
    },

    card: {
        width: width * 0.85,
        backgroundColor: "#fff",
        borderRadius: 12,
        padding: 16,
        marginRight: 16,
        elevation: 4,
    },

    image: {
        width: "100%",
        height: 180,
        borderRadius: 10,
        marginBottom: 12,
    },

    name: {
        fontSize: 18,
        fontWeight: "bold",
        marginBottom: 4,
    },

    price: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#e53935",
        marginBottom: 4,
    },

    meta: {
        color: "#666",
        marginBottom: 8,
    },

    sectionTitle: {
        marginTop: 10,
        fontWeight: "bold",
        fontSize: 15,
    },

    text: {
        fontSize: 14,
        color: "#444",
        marginTop: 2,
    },
});
