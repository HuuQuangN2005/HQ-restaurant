import { View, Text, FlatList, TouchableOpacity, Alert, ActivityIndicator } from "react-native";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useIsFocused, useNavigation } from "@react-navigation/native";
import { authApis, endpoints } from "../../utils/Apis";
import ReservationManagerStyle from "../../styles/ReservationManagerStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";

const ReservationManager = () => {
    const [reservations, setReservations] = useState([]);
    const [loading, setLoading] = useState(false);
    const isFocused = useIsFocused();
    const nav = useNavigation();

    const loadReservations = async () => {
        const token = await AsyncStorage.getItem("access_token");
        if (!token) return;
        try {
            setLoading(true);
            const api = authApis(token);
            const res = await api.get(endpoints['reservations']);
            setReservations(res.data);
        } catch (err) {
            console.log(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isFocused) loadReservations();
    }, [isFocused]);

    const cancelReservation = (uuid) => {
        Alert.alert(
            "Xác nhận",
            "Bạn có chắc muốn từ chối đặt bàn này?",
            [
                { text: "Không", style: "cancel" },
                {
                    text: "Hủy",
                    onPress: async () => {
                        try {
                            const token = await AsyncStorage.getItem("access_token");
                            const api = authApis(token);
                            await api.patch(`${endpoints['reservations']}${uuid}/`,{
                                status: 3
                            });
                            loadReservations();
                        } catch (err) {
                            console.log(err);
                        }
                    }
                }
            ]
        );
    };

    const editReservation = (item) => {
        Alert.alert(
            "Xác nhận đặt bàn",
            "Chuyển trạng thái.",
            [
                { text: "Hủy", style: "cancel" },
                {
                    text: "Xác nhận",
                    onPress: async () => {
                        try {
                            const token = await AsyncStorage.getItem("access_token");
                            const api = authApis(token);
                            await api.patch(
                                `${endpoints['reservations']}${item.uuid}/`,
                                {
                                    status: 2
                                }
                            );

                            loadReservations();
                        } catch (err) {
                            console.log(err);
                        }
                    }
                }
            ]
        );
    };

    const renderItem = ({ item }) => (
        <View style={ReservationManagerStyle.card}>
            <Text style={ReservationManagerStyle.date}>Người đặt: {item.account.username}</Text>

            <Text>
                Thời gian: {new Date(item.date).toLocaleString("vi-VN")}
            </Text>
            <Text>Số người: {item.participants}</Text>
            <Text style={ReservationManagerStyle.status}>
                Trạng thái: {item.status}
            </Text>
            <View style={ReservationManagerStyle.actionRow}>
                <TouchableOpacity
                    style={ReservationManagerStyle.cancelBtn}
                    onPress={() => cancelReservation(item.uuid)}
                >
                    <Text style={ReservationManagerStyle.cancelText}>Hủy</Text>
                </TouchableOpacity>
                <TouchableOpacity
                    style={ReservationManagerStyle.editBtn}
                    onPress={() => editReservation(item)}
                >
                    <Text style={ReservationManagerStyle.editText}>Xác nhận</Text>
                </TouchableOpacity>
            </View>
        </View>
    );

    if (loading)
        return (
            <View style={ReservationManagerStyle.center}>
                <ActivityIndicator size="large" color="#ff7a00" />
            </View>
        );

    return (
        <View style={ReservationManagerStyle.container}>
            <TouchableOpacity onPress={() => nav.goBack()}>
                <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>
            <Text style={ReservationManagerStyle.title}>Quản lý đặt bàn</Text>

            <FlatList
                data={reservations}
                keyExtractor={item => item.uuid}
                renderItem={renderItem}
                ListEmptyComponent={
                    <Text style={ReservationManagerStyle.emptyText}>
                        Bạn chưa có đặt bàn nào
                    </Text>
                }
            />
        </View>
    );
};

export default ReservationManager;
