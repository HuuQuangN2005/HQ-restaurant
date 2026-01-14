import { Image, Text, View } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import HomeStyle from "../../styles/HomeStyle";
import MyStyle from "../../styles/MyStyle";

const Header = () => {
    return(
        <View style={HomeStyle.header}>
            <View style={MyStyle.row}>
                <Image source={{uri: "https://res.cloudinary.com/dx4i4a03w/image/upload/v1767430259/Screenshot_2026-01-03_155037_h2yjxg.png",}} 
                style={HomeStyle.logo}/>
                <Text style={HomeStyle.headerTitle}>Nhà Hàng</Text>
            </View>

            <View style={MyStyle.row}>
                    <Ionicons name="notifications-outline" size={24} color="#333" />
                    <Ionicons name="cart-outline" size={24} color="#333" />
            </View>
        </View>
    )
}

export default Header;