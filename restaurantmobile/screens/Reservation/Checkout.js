import { View, Text, FlatList, TouchableOpacity, TextInput, Alert, ActivityIndicator } from "react-native";
import { useEffect, useState, useMemo } from "react";
import { useNavigation, useRoute } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";

import { authApis, endpoints } from "../../utils/Apis";
import CheckoutStyle from "../../styles/CheckoutStyle";

const Checkout = () => {
    const nav = useNavigation();
    const route = useRoute();
    const { cartFoods } = route.params;

    const [addresses, setAddresses] = useState([]);
    const [selectedAddress, setSelectedAddress] = useState(null);

    const [showNewAddress, setShowNewAddress] = useState(false);
    const [newAddress, setNewAddress] = useState("");

    const [note, setNote] = useState("");
    const [loading, setLoading] = useState(false);
    const [showAddressList, setShowAddressList] = useState(false);

    const [items, setItems] = useState(
        cartFoods.map(item => ({
            ...item,
            quantity: item.quantity ?? 1
        }))
    );


    const totalPrice = useMemo(() => {
        return items.reduce(
            (sum, item) => sum + Number(item.price) * item.quantity,
            0
        );
    }, [items]);


    const increaseQty = (uuid) => {
        setItems(prev =>
            prev.map(i =>
                i.uuid === uuid ? { ...i, quantity: i.quantity + 1 } : i
            )
        );
    };

    const decreaseQty = (uuid) => {
        setItems(prev =>
            prev.map(i =>
                i.uuid === uuid && i.quantity > 1
                    ? { ...i, quantity: i.quantity - 1 }
                    : i
            )
        );
    };


    useEffect(() => {
        const loadAccount = async () => {
            const token = await AsyncStorage.getItem("access_token");
            if (!token) return;

            try {
                const api = authApis(token);
                const res = await api.get("/apis/accounts/me/");
                const addr = res.data.addresses || [];
                setAddresses(addr);
                if (addr.length > 0) setSelectedAddress(addr[0]);
            } catch (err) {
                console.log(err);
            }
        };
        loadAccount();
    }, []);

    const createOrder = async () => {
        const token = await AsyncStorage.getItem("access_token");
        if (!token) {
            Alert.alert("Thông báo", "Bạn cần đăng nhập",[
                { text: "Hủy", style: "cancel" },
                    {
                        text: "Đăng nhập",
                        onPress: () => {
                            nav.navigate("Login", {
                                next: "Checkout",
                                params: { cartFoods: items },
                            });
                        }
                    }
            ]);
            return;
        }

        try {
            setLoading(true);
            const api = authApis(token);
            let addressUuid = selectedAddress?.uuid;
            if (showNewAddress) {
                if (!newAddress.trim()) {
                    Alert.alert("Thiếu địa chỉ", "Vui lòng nhập địa chỉ mới");
                    return;
                }

                const addrRes = await api.post(
                    "/apis/accounts/me/addresses/",
                    { address: newAddress }
                );
                addressUuid = addrRes.data.uuid;
            }

            if (!addressUuid) {
                Alert.alert("Thiếu địa chỉ", "Vui lòng chọn hoặc nhập địa chỉ");
                return;
            }
            const orderData = {
                address: addressUuid,
                note: note,
                details: items.map(item => ({
                    food: item.uuid,
                    quantity: item.quantity
                }))
            };

            await api.post(endpoints['orders'], orderData);
            Alert.alert(
                "Thành công",
                "Đặt hàng thành công!",
                [{ text: "OK", onPress: () => nav.navigate("Main", {
                    screen: "Menu"
                }) }]
            );
        } catch (err) {
            console.log(err);
        } finally {
            setLoading(false);
        }
    };

    const renderItem = ({ item }) => (
        <View style={CheckoutStyle.item}>
            <View style={{ flex: 1 }}>
                <Text style={CheckoutStyle.itemName}>{item.name}</Text>
                <Text style={CheckoutStyle.itemPrice}>
                    {Number(item.price).toLocaleString("vi-VN")}đ
                </Text>
            </View>

            <View style={CheckoutStyle.qtyRow}>
                <TouchableOpacity
                    style={CheckoutStyle.qtyBtn}
                    onPress={() => decreaseQty(item.uuid)}
                >
                    <Text style={CheckoutStyle.qtyText}>−</Text>
                </TouchableOpacity>

                <Text style={CheckoutStyle.qtyValue}>{item.quantity}</Text>

                <TouchableOpacity
                    style={CheckoutStyle.qtyBtn}
                    onPress={() => increaseQty(item.uuid)}
                >
                    <Text style={CheckoutStyle.qtyText}>+</Text>
                </TouchableOpacity>
            </View>
        </View>
    );

    if (loading)
        return (
            <View style={CheckoutStyle.center}>
                <ActivityIndicator size="large" color="#ff7a00" />
            </View>
        );

    return (
        <View style={CheckoutStyle.container}>
            <Text style={CheckoutStyle.title}>Thanh toán</Text>
            <View style={CheckoutStyle.addressWrapper}>
            <View style={CheckoutStyle.addressBox}>
                <Text style={CheckoutStyle.addressLabel}>Địa chỉ giao hàng</Text>

                <View style={CheckoutStyle.addressRow}>
                    <Text
                        style={CheckoutStyle.addressText}
                        numberOfLines={2}
                    >
                        {selectedAddress?.address || "Chưa chọn địa chỉ"}
                    </Text>

                    <TouchableOpacity
                        onPress={() => {
                            setShowAddressList(!showAddressList);
                            setShowNewAddress(false);
                        }}
                    >
                        <Text style={CheckoutStyle.changeText}>Đổi</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {showAddressList && (
                <View style={CheckoutStyle.addressDropdown}>
                    {addresses.map(addr => (
                        <TouchableOpacity
                            key={addr.uuid}
                            style={CheckoutStyle.addressOption}
                            onPress={() => {
                                setSelectedAddress(addr);
                                setShowAddressList(false);
                                setShowNewAddress(false);
                            }}
                        >
                            <Text numberOfLines={2}>{addr.address}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            )}
        </View>


            <TouchableOpacity
                onPress={() => setShowNewAddress(!showNewAddress)}
            >
                <Text style={CheckoutStyle.addNewText}>
                    + Thêm địa chỉ mới
                </Text>
            </TouchableOpacity>

            {showNewAddress && (
                <TextInput
                    placeholder="Nhập địa chỉ mới"
                    value={newAddress}
                    onChangeText={setNewAddress}
                    style={CheckoutStyle.input}
                />
            )}

            <Text style={CheckoutStyle.sectionTitle}>Ghi chú</Text>
            <TextInput
                placeholder="Ghi chú cho đơn hàng (tuỳ chọn)"
                value={note}
                onChangeText={setNote}
                style={CheckoutStyle.input}
            />

            <Text style={CheckoutStyle.sectionTitle}>Món đã chọn</Text>
            <FlatList
                data={items}
                keyExtractor={item => item.uuid}
                renderItem={renderItem}
            />

            <View style={CheckoutStyle.totalRow}>
                <Text style={CheckoutStyle.totalLabel}>Tổng tiền</Text>
                <Text style={CheckoutStyle.totalPrice}>
                    {totalPrice.toLocaleString("vi-VN")}đ
                </Text>
            </View>

            <TouchableOpacity
                style={CheckoutStyle.submitBtn}
                onPress={createOrder}
            >
                <Text style={CheckoutStyle.submitText}>
                    Xác nhận thanh toán
                </Text>
            </TouchableOpacity>
        </View>
    );
};

export default Checkout;
