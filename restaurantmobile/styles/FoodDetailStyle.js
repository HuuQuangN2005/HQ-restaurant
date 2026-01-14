import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        backgroundColor: "#fff",
    },

    goBack: {
        width:"100%",
        fontSize: 28,
        padding: 12,
        color: "#333",
        backgroundColor: "#F2F2F2"
    },

    image: {
        width: "100%",
        height: 260,
    },

    content: {
        padding: 16,
    },

    name: {
        fontSize: 22,
        fontWeight: "bold",
        color: "#222",
    },

    price: {
        fontSize: 20,
        color: "#e53935",
        marginVertical: 6,
        fontWeight: "bold",
    },

    category: {
        color: "#777",
        marginBottom: 10,
    },

    cookTime: {
        marginBottom: 10,
        fontSize: 15,
    },

    description: {
        fontSize: 16,
        lineHeight: 22,
        color: "#444",
    },

    footer: {
        padding: 16,
    },

    addToCartBtn: {
        backgroundColor: "#ff5722",
        paddingVertical: 14,
        borderRadius: 10,
        alignItems: "center",
    },

    addToCartText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "bold",
    },
    commentBox: {
        paddingHorizontal: 10,
        marginTop: 20,
        paddingTop: 10,
        borderTopWidth: 1,
        borderColor: "#ddd"
    },

    commentTitle: {
        fontSize: 18,
        fontWeight: "bold",
        marginBottom: 10
    },

    noComment: {
        color: "#777",
        fontStyle: "italic"
    },

    commentItem: {
        marginBottom: 10
    },

    commentUser: {
        fontWeight: "bold"
    },

    commentContent: {
        marginLeft: 6
    },

    commentInputRow: {
        flexDirection: "row",
        alignItems: "center",
        marginVertical: 10
    },

    commentInput: {
        flex: 1,
        borderWidth: 1,
        borderColor: "#ccc",
        borderRadius: 8,
        padding: 10
    },

    commentSendBtn: {
        marginLeft: 8,
        backgroundColor: "#f5a623",
        paddingVertical: 10,
        paddingHorizontal: 14,
        borderRadius: 8
    },

    commentSendText: {
        color: "#fff",
        fontWeight: "bold"
    },
    loadMoreBtn: {
        alignSelf: "center",
        marginVertical: 12
    },
    loadMoreText: {
        color: "#f5a623",
        fontWeight: "bold"
    },

});
