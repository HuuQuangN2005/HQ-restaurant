import { Image, ScrollView, Text, TouchableOpacity, View } from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";
import CompareFoodStyle from "../../styles/CompareFoodStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";

const CompareFood = () => {
    const route = useRoute();
    const { foods } = route.params;
    const nav = useNavigation();

    const [food1, food2] = foods;

    const renderFood = (food) => (
        <View style={CompareFoodStyle.card}>
            <Image
                source={{ uri: food.image }}
                style={CompareFoodStyle.image}
            />

            <Text style={CompareFoodStyle.name}>{food.name}</Text>

            <Text style={CompareFoodStyle.price}>
                {Number(food.price).toLocaleString("vi-VN")}đ
            </Text>

            <Text style={CompareFoodStyle.meta}>
                ⏱ {food.cook_time} phút
            </Text>

            <Text style={CompareFoodStyle.sectionTitle}>Nguyên liệu</Text>
            {food.ingredients?.map((ing, idx) => (
                <Text key={idx} style={CompareFoodStyle.text}>
                    • {ing}
                </Text>
            ))}

            <Text style={CompareFoodStyle.sectionTitle}>Mô tả</Text>
            <Text style={CompareFoodStyle.text}>
                {food.description || "Chưa có mô tả"}
            </Text>
        </View>
    );

    return (
        <View>
            <TouchableOpacity onPress={() => nav.goBack()}>
                    <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>
            <ScrollView horizontal>
                <View style={CompareFoodStyle.container}>
                    {renderFood(food1)}
                    {renderFood(food2)}
                </View>
            </ScrollView>
        </View>
        
    );
};

export default CompareFood;
