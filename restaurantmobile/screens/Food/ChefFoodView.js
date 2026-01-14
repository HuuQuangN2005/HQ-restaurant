import { Image, ScrollView, Text, TouchableOpacity, View } from "react-native";
import { useEffect, useState } from "react";
import { useNavigation, useRoute } from "@react-navigation/native";
import Apis, { endpoints } from "../../utils/Apis";
import MyStyle from "../../styles/MyStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";

const ChefFoodView = () => {
    const route = useRoute();
    const { foodUuid } = route.params;
    const navigation = useNavigation();

    const [food, setFood] = useState(null);
    const [comments, setComments] = useState([]);

    const [loading, setLoading] = useState(false);
    const [commentPage, setCommentPage] = useState(1);
    const [hasNext, setHasNext] = useState(true);
    const [loadingComment, setLoadingComment] = useState(false);

    const loadFoodDetail = async () => {
        try {
            setLoading(true);
            const res = await Apis.get(`${endpoints['foods']}${foodUuid}/`);
            setFood(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const loadComments = async (page = 1) => {
        if (loadingComment) return;
        if (!hasNext && page !== 1) return;

        try {
            setLoadingComment(true);

            const res = await Apis.get(
                `${endpoints['foods']}${foodUuid}/comments/`,
                { params: { page } }
            );

            const results = res.data.results || [];

            if (page === 1) {
                setComments(results);
            } else {
                setComments(prev => [...prev, ...results]);
            }

            setHasNext(!!res.data.next);
            setCommentPage(page);
        } catch (err) {
            console.error(err);
        } finally {
            setLoadingComment(false);
        }
    };

    useEffect(() => {
        loadFoodDetail();
        setComments([]);
        setCommentPage(1);
        setHasNext(true);
        loadComments(1);
    }, [foodUuid]);

    if (loading || !food) {
        return (
            <View style={MyStyle.center}>
                <Text>Đang tải dữ liệu...</Text>
            </View>
        );
    }

    return (
        <ScrollView style={FoodDetailStyle.container}>
            <TouchableOpacity onPress={() => navigation.goBack()}>
                <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>

            <Image
                source={{ uri: food.image }}
                style={FoodDetailStyle.image}
                resizeMode="cover"
            />

            <View style={FoodDetailStyle.content}>
                <Text style={FoodDetailStyle.name}>{food.name}</Text>

                <Text style={FoodDetailStyle.price}>
                    {Number(food.price).toLocaleString("vi-VN")}đ
                </Text>

                <Text style={FoodDetailStyle.cookTime}>
                    Thời gian nấu: {food.cook_time} phút
                </Text>

                <Text style={FoodDetailStyle.description}>
                    {food.description || "Chưa có mô tả"}
                    {"\n"}Nguyên liệu: {food.ingredients.join(", ")}
                </Text>
            </View>

            <View style={FoodDetailStyle.commentBox}>
                <Text style={FoodDetailStyle.commentTitle}>
                    Đánh giá & bình luận
                </Text>

                {comments.length === 0 && (
                    <Text style={FoodDetailStyle.noComment}>
                        Chưa có bình luận nào
                    </Text>
                )}

                {comments.map(c => (
                    <View key={c.uuid} style={FoodDetailStyle.commentItem}>
                        <Text style={FoodDetailStyle.commentUser}>
                            {c.account?.first_name || c.account?.username || "Khách"}
                        </Text>
                        <Text style={FoodDetailStyle.commentContent}>
                            {c.content}
                        </Text>
                    </View>
                ))}

                {hasNext && (
                    <TouchableOpacity
                        style={FoodDetailStyle.loadMoreBtn}
                        onPress={() => loadComments(commentPage + 1)}
                    >
                        <Text style={FoodDetailStyle.loadMoreText}>
                            {loadingComment ? "Đang tải..." : "Xem thêm"}
                        </Text>
                    </TouchableOpacity>
                )}
            </View>
        </ScrollView>
    );
};

export default ChefFoodView;
