import { Alert, Image, KeyboardAvoidingView, Platform, ScrollView, Text, TextInput, TouchableOpacity, View } from "react-native";
import { useContext, useEffect, useState } from "react";
import { useNavigation, useRoute } from "@react-navigation/native";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import MyStyle from "../../styles/MyStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Ionicons } from "@expo/vector-icons";
import ChefStyle from "../../styles/ChefStyle";
import { MyUserContext } from "../../utils/MyContext";

const FoodDetail = () => {
    const route = useRoute();
    const { foodUuid } = route.params;
    const [food, setFood] = useState();
    const nav = useNavigation();
    const [loading, setLoading] = useState(false);
    const [comments, setComments] = useState([]);
    const [commentText, setCommentText] = useState("");

    const [commentPage, setCommentPage] = useState(1);
    const [hasNextComment, setHasNextComment] = useState(true);
    const [loadingComment, setLoadingComment] = useState(false);
    const [user] = useContext(MyUserContext);

    const loadFoodDetail = async () => {
        setLoading(true)
        try {
            let res = await Apis.get(`${endpoints['foods']}${foodUuid}/`);
            setFood(res.data);
        } catch (err) {
            console.error("Lỗi:", err);
        }
        finally{
            setLoading(false);
        }
    };

    const loadComments = async (page = 1) => {
        if (loadingComment) return;
        if (!hasNextComment && page !== 1) return;

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
            setHasNextComment(!!res.data.next);
            setCommentPage(page);
        } catch (err) {
            console.error("Lỗi:", err);
        } finally {
            setLoadingComment(false);
        }
    };

    const addComment = async () => {
        if (!commentText.trim()) return;

        try {
            const token = await AsyncStorage.getItem("access_token");
            if (!token) {
                Alert.alert(
                    "Thông báo",
                    "Bạn cần đăng nhập để bình luận.",
                    [
                        { text: "Hủy", style: "cancel" },
                        {
                            text: "Đăng nhập",
                            onPress: () => {
                                nav.navigate("Login", {
                                    next: "FoodDetail",
                                    params: { foodUuid },
                                });
                            }
                        }
                    ]
                );
                return;
            }

            const api = authApis(token);
            await api.post(
                `${endpoints['foods']}${foodUuid}/comments/`,
                { content: commentText }
            );

            setCommentText("");
            setHasNextComment(true);
            loadComments(1);
        } catch (err) {
            console.error("Lỗi:", err);
        }
    };

    useEffect(() => {
        loadFoodDetail();
        setComments([]);
        setCommentPage(1);
        setHasNextComment(true);
        loadComments(1);
    }, [foodUuid]);

    const deleteComment = async (commentUuid) => {
        try {
            const token = await AsyncStorage.getItem("access_token");
            if (!token) {
                Alert.alert("Thông báo", "Bạn cần đăng nhập để thực hiện thao tác này");
                return;
            }

            Alert.alert(
                "Xác nhận",
                "Bạn có chắc muốn xóa bình luận này?",
                [
                    { text: "Hủy", style: "cancel" },
                    {
                        text: "Xóa",
                        style: "destructive",
                        onPress: async () => {
                            const api = authApis(token);
                            await api.delete(`/apis/comments/${commentUuid}/`);
                            loadComments(1);
                        }
                    }
                ]
            );

        } catch (err) {
            console.log(err.response?.data || err);
            Alert.alert("Lỗi", "Không thể xóa bình luận");
        }
    };

    if (loading)
        return (
            <View style={MyStyle.center}>
                <Text> Đang tải món ăn...</Text>
            </View>
    );

    if (!food)
        return (
            <View style={MyStyle.center}>
                <Text>Không tìm thấy món ăn</Text>
            </View>
    );


    return (
        <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
        <ScrollView
            style={FoodDetailStyle.container}
            keyboardShouldPersistTaps="handled"
        >

            <TouchableOpacity onPress={() => nav.goBack()}>
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

                <Text style={FoodDetailStyle.category}>
                    Danh mục: {food.category}
                </Text>

                <Text style={FoodDetailStyle.cookTime}>
                    Thời gian nấu: {food.cook_time} phút
                </Text>

                <Text style={FoodDetailStyle.description}>
                    {food.description}
                    {"\n"}Nguyên liệu: {food.ingredients.join(", ")} 
                </Text>
            </View>
            

            <View style={FoodDetailStyle.footer}>
                <TouchableOpacity style={FoodDetailStyle.addToCartBtn}>
                    <Text style={FoodDetailStyle.addToCartText}>
                        Thêm vào giỏ hàng
                    </Text>
                </TouchableOpacity>
            </View>

            <View style={FoodDetailStyle.commentBox}>
                <Text style={FoodDetailStyle.commentTitle}>Bình luận</Text>

                {comments.length === 0 && (
                    <Text style={FoodDetailStyle.noComment}>
                        Chưa có bình luận nào
                    </Text>
                )}

                <View style={FoodDetailStyle.commentInputRow}>
                    <TextInput
                        placeholder="Nhập bình luận..."
                        value={commentText}
                        onChangeText={setCommentText}
                        style={FoodDetailStyle.commentInput}
                    />

                    <TouchableOpacity
                        onPress={addComment}
                        style={FoodDetailStyle.commentSendBtn}
                    >
                        <Text style={FoodDetailStyle.commentSendText}>
                            Gửi
                        </Text>
                    </TouchableOpacity>
                </View>

                {comments.map(c => (
                    <View key={c.uuid} style={FoodDetailStyle.commentItem}>
                        <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
                            <Text style={FoodDetailStyle.commentUser}>
                                {c.account.username}
                            </Text>
                            {user?.username === c.account.username && (
                                <TouchableOpacity
                                    style={ChefStyle.actionBtn}
                                    onPress={() => deleteComment(c.uuid)}>
                                    <Ionicons name="trash-outline" size={22} color="#d32f2f" />
                                </TouchableOpacity>
                            )}
                        </View>
                        <Text style={FoodDetailStyle.commentContent}>
                            {c.content}
                        </Text>
                    </View>
                ))}

                {hasNextComment && (
                    <TouchableOpacity
                        style={FoodDetailStyle.loadMoreBtn}
                        onPress={() => loadComments(commentPage + 1)}
                    >
                        <Text style={FoodDetailStyle.loadMoreText}>
                            {loadingComment ? "Đang tải..." : "Xem thêm bình luận"}
                        </Text>
                    </TouchableOpacity>
                )}
            </View>
        </ScrollView>
    </KeyboardAvoidingView>
    );
};

export default FoodDetail;
