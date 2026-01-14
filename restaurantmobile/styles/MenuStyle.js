import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        backgroundColor: "#fff",
        flex: 1,
    },

    searchTypeWrapper: {
        marginHorizontal: 12,
        marginBottom: 8,
    },

    searchTypeButton: {
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        padding: 12,
        backgroundColor: "#fafafa",
    },

    searchTypeButtonText: {
        fontSize: 15,
        fontWeight: "500",
        color: "#333",
    },

    searchTypeDropdown: {
        marginTop: 6,
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        backgroundColor: "#fff",
        overflow: "hidden",
    },

    searchTypeItem: {
        padding: 12,
        backgroundColor: "#fff",
        borderBottomWidth: 1,
        borderBottomColor: "#eee",
    },

    searchTypeItemActive: {
        backgroundColor: "#ffe082",
    },

    title: {
        fontSize: 24,
        fontWeight: "bold",
        marginHorizontal: 16,
        marginVertical: 16,
    },

    categoryList: {
        marginTop: 20,
        flexDirection: "row",
        paddingHorizontal: 10,
        marginBottom: 16,
    },

    cateFilter: {
        paddingHorizontal: 14,
        paddingVertical: 8,
        marginHorizontal: 6,
        borderRadius: 20,
        backgroundColor: "#eee",
    },

    cateActive: {
        backgroundColor: "#ffd54f",
    },

    sortRowWrapper: {
        marginHorizontal: 12,
        marginBottom: 8,
    },

    sortRowHeader: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
    },

    sortButton: {
        flex: 1,
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        paddingVertical: 12,
        paddingHorizontal: 12,
        backgroundColor: "#fafafa",
    },

    sortButtonText: {
        fontSize: 15,
        fontWeight: "500",
        color: "#333",
    },

    compareTopBtn: {
        paddingVertical: 12,
        paddingHorizontal: 14,
        borderRadius: 8,
        backgroundColor: "#ff5722",
    },

    compareTopText: {
        color: "#fff",
        fontSize: 14,
        fontWeight: "600",
    },

    sortDropdown: {
        marginTop: 6,
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        backgroundColor: "#fff",
        overflow: "hidden",
    },

    sortItem: {
        padding: 12,
        borderBottomWidth: 1,
        borderBottomColor: "#eee",
        backgroundColor: "#fff",
    },

    foodItem: {
        flexDirection: "row",
        alignItems: "center",
        marginHorizontal: 16,
        marginBottom: 12,
        backgroundColor: "#f9f9f9",
        borderRadius: 10,
        padding: 10,
        paddingBottom: 40,
    },

    foodItemSelected: {
        borderWidth: 2,
        borderColor: "#ff5722",
    },

    foodImage: {
        width: 70,
        height: 70,
        borderRadius: 8,
        marginRight: 12,
        backgroundColor: "#eee",
    },

    foodInfo: {
        flex: 1,
        justifyContent: "center",
    },

    foodName: {
        fontSize: 16,
        fontWeight: "600",
        color: "#111",
    },

    foodPrice: {
        marginTop: 4,
        fontSize: 15,
        color: "#e53935",
        fontWeight: "bold",
    },

    foodMeta: {
        color: "#777",
        marginTop: 4,
        marginLeft: 5
    },

    search: {
        margin: 12,
        padding: 10,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: "#ddd",
        backgroundColor: "#fff",
    },

    actionRow: {
        position: "absolute",
        bottom: 8,
        right: 8,
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
    },

    compareBtn: {
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 16,
        backgroundColor: "#eee",
    },

    compareBtnSelected: {
        backgroundColor: "#ff5722",
    },

    compareText: {
        color: "#333",
        fontWeight: "500",
        fontSize: 13,
    },

    compareTextSelected: {
        color: "#fff",
    },

    addCartPlus: {
        width: 28,
        height: 28,
        borderRadius: 14,
        backgroundColor: "#e5e7eb",
        alignItems: "center",
        justifyContent: "center",
    },

    addCartPlusActive: {
        backgroundColor: "#22c55e",
    },

    addCartPlusText: {
        fontSize: 18,
        fontWeight: "bold",
        color: "#374151",
        lineHeight: 20,
        textAlign: "center",
    },

    addCartPlusTextActive: {
        color: "#fff",
    },

    compareFooterBtn: {
        position: "absolute",
        bottom: 16,
        left: 16,
        right: 16,
        backgroundColor: "#13c922ff",
        paddingVertical: 14,
        borderRadius: 10,
        alignItems: "center",
        elevation: 6,
    },

    compareFooterText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "bold",
    },
});
