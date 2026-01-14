import { useCallback, useContext, useEffect, useState } from "react";
import { Alert, FlatList, Image, Text, TouchableOpacity, View } from "react-native";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import { MyUserContext } from "../../utils/MyContext";
import ChefStyle from "../../styles/ChefStyle";
import { Ionicons } from "@expo/vector-icons";
import { useFocusEffect, useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import FoodDetailStyle from "../../styles/FoodDetailStyle";

const ChefFoodManager = () => {
    const [user] = useContext(MyUserContext);
    const [foods, setFoods] = useState([]);
    const navigation = useNavigation()

    const loadFoods = async () => {
        try{
            const token = await AsyncStorage.getItem("access_token");
            if (!token) return;

            const api = authApis(token);
            let res = await api.get(endpoints["foods"], { params: { chef: user.uuid }});
            setFoods(res.data.results || []);
        }
        catch(ex){
            console.error(ex);
        }
    };

    useFocusEffect(
        useCallback(() => {
            loadFoods();
        }, [user])
    );

    const deleteFood = async (foodId) => {
        try {
            const token = await AsyncStorage.getItem("access_token");
            const api = authApis(token);
            await api.delete(`${endpoints['foods']}${foodId}/`);
            setFoods(prev => prev.filter(f => f.uuid !== foodId));
        } catch (ex) {
            console.error(ex);
        }
    };

    const confirmDelete = (foodId) => {
        Alert.alert(
            "Xóa món ăn",
            "Bạn chắc chắn muốn xóa món này?",
            [
                { text: "Hủy", style: "cancel" },
                { text: "Xóa", style: "destructive", onPress: () => deleteFood(foodId) }
            ]
        );
    };

    const renderItem = ({ item }) => (
        <View style={ChefStyle.foodItem}>
            <TouchableOpacity
            style={ChefStyle.foodMain}
            activeOpacity={0.8}
            onPress={() =>
                navigation.navigate("ChefFoodView", {
                    foodUuid: item.uuid
                })
            }>
            <Image source={{ uri: item.image }} style={ChefStyle.foodImage}/>

            <View style={ChefStyle.foodInfo}>
                <Text style={ChefStyle.foodName}>{item.name}</Text>
                <Text style={ChefStyle.foodPrice}>
                    {Number(item.price).toLocaleString("vi-VN")}đ
                </Text>
            </View>
            
        </TouchableOpacity>

            <TouchableOpacity
                style={ChefStyle.actionBtn}
                onPress={() =>
                    navigation.navigate("CreateFood", {
                        foodId: item.uuid,
                        isEdit: true
                    })
                }>
                <Ionicons name="create-outline" size={22} color="#555" />
            </TouchableOpacity>

            <TouchableOpacity
                style={ChefStyle.actionBtn}
                onPress={() => confirmDelete(item.uuid)}>
                <Ionicons name="trash-outline" size={22} color="#d32f2f" />
            </TouchableOpacity>
        </View>
    );

    return(
        <View style={ChefStyle.container}>
            <TouchableOpacity onPress={() => navigation.goBack()}>
                <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>
            <View style={ChefStyle.header}>
                <Text style={ChefStyle.headerTitle}>
                    Món ăn của nhà hàng
                </Text>

                <TouchableOpacity onPress={() => navigation.navigate("CreateFood")}>
                    <Ionicons name="add-circle" size={32} color="#f5a623" />
                </TouchableOpacity>
            </View>

            <FlatList
                data={foods}
                keyExtractor={(item) => item.uuid}
                renderItem={renderItem}
                contentContainerStyle={{ paddingBottom: 20 }}
                ListEmptyComponent={
                    <Text style={ChefStyle.emptyText}>
                        Bạn chưa tạo món ăn nào
                    </Text>
                }
            />
        </View>
    )
}

export default ChefFoodManager;