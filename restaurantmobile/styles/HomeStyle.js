import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1
    },

    content: {
        paddingHorizontal: 16,
    },

    header: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        paddingVertical: 10,
        width:"100%",
        marginTop: 10
    },

    headerTitle: {
        fontSize: 22,
        fontWeight: "bold",
    },

    logo: {
        width: 30,
        height: 30,
        resizeMode: "contain",
        marginRight: 8
    },

    banner: {
        height: 180,
        width: '100%',
        marginTop: 12
    },

    bannerImage: {
        borderRadius: 16,
    },

    //Phan Trang

    pagination: {
        justifyContent: "space-between",
        alignItems: "center",
        paddingHorizontal: 20,
        marginTop: 10,
    },

    pageBtn: {
        paddingVertical: 8,
        paddingHorizontal: 12,
        borderRadius: 10,
        backgroundColor: "#f2eee9",
    },

    pageBtnText: {
        color: "#6F4E37",
        fontWeight: "bold",
    },

    pageText: {
        fontWeight: "600",
        color: "#333",
    },

    //Categories

    categoryItem: {
        width: '25%',
        alignItems: "center",
        marginBottom: 20,
    },

    categoryImage: {
        width: 48,
        height: 48,
        borderRadius: 10,
        resizeMode: "cover",
        backgroundColor: "#f2f2f2",
    },

    categoryText: {
        fontSize: 12,
        marginTop: 6,
        textAlign: "center",
        color: "#333",
    },

    //Product
    ProductContainer: {
        backgroundColor: "#e9bc1aff",
        paddingVertical: 12,
        marginTop: 16,
        borderRadius: 10,
    },

    ProductHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginBottom: 10,
    },

    ProductTitle: {
        marginLeft: 10,
        fontWeight: "900",
        fontSize: 20
    },

    ProductViewAll: {
        marginRight: 10,
        color: "#438bb2ff",
        fontWeight: "bold",
    },
    ProductCard: {
        width: 160,
        marginRight: 12,
        backgroundColor: "#fff",
        borderRadius: 12,
        padding: 10,
    },

    ProductImage: {
        width: "100%",
        height: 100,
        borderRadius: 10,
    },
    ProductName: {
        marginTop: 6,
        fontSize: 14,
        fontWeight: "600",
    },
    ProductPrice: {
        color: "#f4511e",
        fontWeight: "bold",
        marginVertical: 4,
    },
    
    AddToCartBtn: {
        marginTop: 6,
        backgroundColor: "#ffe0b2",
        paddingVertical: 6,
        borderRadius: 8,
    },

    ShowDetails: {
        textAlign: "center",
        color: "#fb8c00",
        fontSize: 12,
        fontWeight: "bold",
    },  

});