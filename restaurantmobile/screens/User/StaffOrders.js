import { View, Text, FlatList, TouchableOpacity, Alert, ActivityIndicator } from "react-native";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useIsFocused, useNavigation } from "@react-navigation/native";

import { authApis, endpoints } from "../../utils/Apis";
import StaffOrderStyle from "../../styles/StaffOrderStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";

const StaffOrders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const isFocused = useIsFocused();
    const nav = useNavigation();

    const loadOrders = async () => {
        const token = await AsyncStorage.getItem("access_token");
        if (!token) return;

        try {
            setLoading(true);
            const api = authApis(token);
            const res = await api.get(endpoints['orders']);
            const simpleOrders = res.data.results || [];

            const detailOrders = await Promise.all(
                simpleOrders.map(async (o) => {
                    const detailRes = await api.get(
                        `${endpoints['orders']}${o.uuid}/`
                    );
                    return detailRes.data;
                })
            );

            setOrders(detailOrders);
        } catch (err) {
            console.log(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isFocused) loadOrders();
    }, [isFocused]);

    const confirmPaid = (order) => {
        Alert.alert(
            "Xác nhận",
            "Đánh dấu đơn này đã thanh toán?",
            [
                { text: "Hủy", style: "cancel" },
                {
                    text: "Xác nhận",
                    onPress: async () => {
                        try {
                            const token = await AsyncStorage.getItem("access_token");
                            const api = authApis(token);

                            await api.patch(
                                `${endpoints['orders']}${order.uuid}/`,
                                { is_paid: true, status: 2 }
                            );

                            loadOrders();
                        } catch (err) {
                            console.log(err);
                        }
                    }
                }
            ]
        );
    };

    const cancelOrder = (uuid) => {
        Alert.alert(
            "Xác nhận",
            "Bạn có chắc muốn hủy đơn hàng này?",
            [
                { text: "Không", style: "cancel" },
                {
                    text: "Hủy",
                    style: "destructive",
                    onPress: async () => {
                        try {
                            const token = await AsyncStorage.getItem("access_token");
                            const api = authApis(token);

                            await api.patch(
                                `${endpoints['orders']}${uuid}/`,
                                { status: 3 }
                            );

                            loadOrders();
                        } catch (err) {
                            console.log(err);
                        }
                    }
                }
            ]
        );
    };

    const renderItem = ({ item }) => {
        const isCanceled = item.status === "Cancelled";
        const isPaid = item.status === "Completed";
        return(
            <View style={StaffOrderStyle.card}>
            <Text style={StaffOrderStyle.id}>Mã đơn: {item.uuid}</Text>

            <View style={StaffOrderStyle.row}>
                <Text style={StaffOrderStyle.label}>Khách:</Text>
                <Text style={StaffOrderStyle.value}>{item.account.username}</Text>
            </View>

            <View style={StaffOrderStyle.row}>
                <Text style={StaffOrderStyle.label}>Tổng tiền:</Text>
                <Text style={StaffOrderStyle.price}>
                    {Number(item.total_price).toLocaleString("vi-VN")}đ
                </Text>
            </View>
            <View
                style={[
                    StaffOrderStyle.badge,
                    isCanceled
                        ? StaffOrderStyle.badgeCanceled
                        : isPaid
                        ? StaffOrderStyle.badgePaid
                        : StaffOrderStyle.badgeUnpaid
                ]}
            >
                <Text
                    style={[
                        StaffOrderStyle.badgeText,
                        isCanceled
                            ? StaffOrderStyle.badgeTextCanceled
                            : isPaid
                            ? StaffOrderStyle.badgeTextPaid
                            : StaffOrderStyle.badgeTextUnpaid
                    ]}
                >
                    {isCanceled
                        ? "Đã hủy"
                        : isPaid
                        ? "Đã thanh toán"
                        : "Chưa thanh toán"}
                </Text>
            </View>


            {item.status === "Pending" && (
                <View style={StaffOrderStyle.row}>
                    <TouchableOpacity onPress={() => cancelOrder(item.uuid)}>
                        <Text style={StaffOrderStyle.cancelText}>Hủy đơn hàng</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        style={StaffOrderStyle.payBtn}
                        onPress={() => confirmPaid(item)}
                    >
                        <Text style={StaffOrderStyle.payText}>Xác nhận đã thanh toán</Text>
                    </TouchableOpacity>
                </View>
            )}
        </View>
        )
    };

    if (loading)
        return (
            <View style={StaffOrderStyle.center}>
                <ActivityIndicator size="large" color="#ff7a00" />
            </View>
        );

    return (
        <View style={StaffOrderStyle.container}>
            <TouchableOpacity onPress={() => nav.goBack()}>
                <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>
            <Text style={StaffOrderStyle.title}>
                Quản lý thanh toán (Staff)
            </Text>

            <FlatList
                data={orders}
                keyExtractor={(item) => item.uuid}
                renderItem={renderItem}
                ListEmptyComponent={
                    <Text style={StaffOrderStyle.empty}>
                        Không có đơn hàng
                    </Text>
                }
            />
        </View>
    );
};

export default StaffOrders;
