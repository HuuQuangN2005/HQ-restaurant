import MyStyle from './styles/MyStyle';
import Home from './screens/Home/Home';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaView } from 'react-native-safe-area-context';
import Menu from './screens/Food/Menu';
import { NavigationContainer } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import Profile from './screens/User/Profile';
import Login from './screens/User/Login';
import Register from './screens/User/Register';
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useContext, useReducer } from "react";
import MyUserReducer from './reducers/MyUserReducer';
import { MyUserContext } from "./utils/MyContext";
import FoodDetail from './screens/Food/FoodDetail';
import ChefFoodManager from './screens/Food/ChefFoodManager';
import CreateFood from './screens/Food/CreateFood';
import CompareFood from './screens/Food/CompareFood';
import Reservation from './screens/Reservation/Reservation';
import ChefProfile from './screens/User/ChefProfile';
import ChefFoodView from './screens/Food/ChefFoodView';
import Checkout from './screens/Reservation/Checkout';
import ReservationManager from './screens/Reservation/ReservationManager';
import StaffManager from './screens/User/StaffManager';
import StaffOrders from './screens/User/StaffOrders';


const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const TabNavigator = () => {
  const [user, ] = useContext(MyUserContext);
  return(
    <Tab.Navigator>
      <Tab.Screen name='Home' component={Home} options={{
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen name='Search' component={Menu} options={{
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="search-outline" size={size} color={color} />
          ),
        }}
      />
      {user ? (
        <Tab.Screen
          name="Profile"
          component={Profile}
          options={{
            headerShown: false,
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="person-outline" size={size} color={color} />
            ),
          }}
        />
      ) : (
        <>
          <Tab.Screen
            name="Login"
            component={Login}
            options={{
              headerShown: false,
              tabBarIcon: ({ color, size }) => (
                <Ionicons name="log-in-outline" size={size} color={color} />
              ),
            }}
          />
        </>
      )}
    </Tab.Navigator>

  );
};

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return(
    <SafeAreaView style={MyStyle.container}>
      <MyUserContext.Provider value={[user, dispatch]}>
        <NavigationContainer>
          <Stack.Navigator screenOptions={{ headerShown: false, animation: "slide_from_right", }}>
            <Stack.Screen name='Main' component={TabNavigator} />
            <Stack.Screen name='Login' component={Login} />
            <Stack.Screen name='Register' component={Register} />
            <Stack.Screen name="FoodDetail" component={FoodDetail}/>
            <Stack.Screen name="ChefFoodManager" component={ChefFoodManager}/>
            <Stack.Screen name="CreateFood" component={CreateFood} />
            <Stack.Screen name="CompareFood" component={CompareFood}/>
            <Stack.Screen name="Reservation" component={Reservation} />
            <Stack.Screen name="ChefProfile" component={ChefProfile} />
            <Stack.Screen name="ChefFoodView" component={ChefFoodView} />
            <Stack.Screen name="Checkout" component={Checkout} />
            <Stack.Screen name="ReservationManager" component={ReservationManager}/>
            <Stack.Screen name="StaffManager" component={StaffManager}/>
            <Stack.Screen name="StaffOrders" component={StaffOrders}/>
          </Stack.Navigator>
        </NavigationContainer>
      </MyUserContext.Provider>
    </SafeAreaView>
  )
}

export default App;