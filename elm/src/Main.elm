module Main exposing (..)

import Browser
import Html             exposing (..)
import Html.Attributes  exposing (..)
import Html.Events      as HE

type Action = Look
            | Take
            | Drop
            | Open
            | Close
            | Read
            | Write
            | Break
            | Lock
            | Unlock

type alias Usage = List Action
type alias Property = (Action, String)

type alias Object =
    { name          :   String
    , usage         :   Usage
    , properties    :   List Property
    }

type alias Place =
    { name      :   String
    , current   :   Bool
    , objects   :   List Object
    }

type alias Map = List (List Place)

type alias World =
    { map   :   Map
    , time  :   Int
    }

type alias Model =
    { display   :   String
    , world     :   World
    }

type Msg = Input String
         | Output String


--
--  World Map and Design
--

--  00   South-East Corner
place00 : Place
place00 = Place
    "South-East Corner"
    False
    []

--  01   Thekkini
place01 : Place
place01 = Place
    "Thekkini"
    False
    []

--  02  South-West Corner
place02 : Place
place02 = Place
    "South-West Corner"
    False
    []

--  10  Kizhakkini
place10 : Place
place10 = Place
    "Kizhakkini"
    False
    []

--  11  Nadumuttam
place11 : Place
place11 = Place
    "Nadumuttam"
    False
    []

--  12  Padinjarini
place12 : Place
place12 = Place
    "Padinjarini"
    False
    []

--  20  North-East Corner
place20 : Place
place20 = Place
    "North-East Corner"
    False
    []

--  21  Vadakkini
place21 : Place
place21 = Place
    "Vadakkini"
    False
    []

--  22  North-West Corner
place22 : Place
place22 = Place
    "North-West Corner"
    False
    []


worldMap : Map
worldMap =
    [ [ place00, place01, place02 ]
    , [ place10, place11, place12 ]
    , [ place20, place21, place22 ]
    ]



--
--  Core functions.
--

view : Model -> Html Msg
view model =
    div [ id "main" ]
        [ div [ id "display" ]
            [ text model.display
            ]
        ]
    

update : Msg -> Model -> (Model, Cmd Msg)
update msg model = (model, Cmd.none)

initialModel : Model
initialModel = Model
                   """
                   Welcome to Pappdam World.
                   You are in a nalukettu.  One that had been built perhaps
                   300-400 years ago.
                   """
                   (World worldMap 0)

init : () -> (Model, Cmd Msg)
init _ = (initialModel, Cmd.none)

main : Program () Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = \_ -> Sub.none
    , view = view
    }
