module Main exposing (..)

import Browser
import Html             exposing (..)
import Html.Attributes  exposing (..)
import Html.Events      exposing (..)
import List             exposing (..)
import Maybe            exposing (..)

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
    { position      :   (Int, Int)
    , name          :   String
    , current       :   Bool
    , description   :   String
    , objects       :   List Object
    }

emptyPlace : Place
emptyPlace = Place (0,0) "" False "" []

type alias Map = List (List Place)

type alias World =
    { map   :   Map
    , time  :   Int
    }

type alias Model =
    { display   :   Html Msg
    , world     :   World
    }

type Msg = Input String
         | Output String


--
--  World Map and Design
--

--  00   South-East Corner
place00 : Place
place00 = Place (-1,1)
    "South-East Corner"
    False
    ""
    []

--  01   Thekkini
place01 : Place
place01 = Place (0,1)
    "Thekkini"
    False
    """
    This is a mysterious chamber and retains an eerie distrubing ambience.  The
    rumours are long of the histories.  It lies in dark, sleeping like a beast.
    """
    []

--  02  South-West Corner
place02 : Place
place02 = Place (1,1)
    "South-West Corner"
    False
    ""
    []

--  10  Kizhakkini
place10 : Place
place10 = Place (-1,0)
    "Kizhakkini"
    False
    ""
    []

--  11  Nadumuttam
place11 : Place
place11 = Place (0,0)
    "Nadumuttam"
    True
    """
    The nadumuttam is a place brimming in sunlight.  A pool congeals here during
    the unabated rains of the monsoon.  A tulsi plant stands lonely in the
    centre.
    """
    []

--  12  Padinjarini
place12 : Place
place12 = Place (0,1)
    "Padinjarini"
    False
    ""
    []

--  20  North-East Corner
place20 : Place
place20 = Place (-1,-1)
    "North-East Corner"
    False
    ""
    []

--  21  Vadakkini
place21 : Place
place21 = Place (0,-1)
    "Vadakkini"
    False
    ""
    []

--  22  North-West Corner
place22 : Place
place22 = Place (1,-1)
    "North-West Corner"
    False
    ""
    []

--  The World Map.
worldMap : Map
worldMap =
    [ [ place00, place01, place02 ]
    , [ place10, place11, place12 ]
    , [ place20, place21, place22 ]
    ]

--  The current position in the map.
-- describeCurrentPlace : Map -> String
currentPlace theMap =
    let
        getPlace xs = filter (\x -> x.current) xs
    in  concat <| List.map getPlace theMap

--  Describe a place.
describeCurrentPlace : Map -> Html Msg
describeCurrentPlace theMap =
    let
        place = withDefault emptyPlace (head <| currentPlace theMap)
    in
        div [ class "place-desc" ]
            [ b [] [ text place.name ]
            , br [] []
            , text place.description
            ]
    


--
--  Core functions.
--

--  VIEW.
view : Model -> Html Msg
view model =
    div [ id "main" ]
        [ div [ id "display" ]
            [ model.display
            , br [] []
            , div [ id "input-area" ]
                [ label [ id "promp-text" ] [ text ">" ]
                , input [ id "prompt", onInput Input ] []
                ]
            ]
        ]
    
--  UPDATE.
update : Msg -> Model -> (Model, Cmd Msg)
update msg model = (model, Cmd.none)

--  INITAL MODEL AND INIT.
initDisplay : Html Msg
initDisplay = div [] 
                [   text <|
                    """
                    You are in a nalukettu.  One that had been built perhaps
                    300–400 years ago.  You have happened upon this ancient
                    edifice in a fit of desperate escape.  Who might have
                    built such grand a house for themselves you do not
                    know; you are yet compelled to enter.
                    """
                , br [] []
                , describeCurrentPlace worldMap
                ]

initialModel : Model
initialModel = Model initDisplay (World worldMap 0)

init : () -> (Model, Cmd Msg)
init _ = (initialModel, Cmd.none)

--  MAIN.
main : Program () Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = \_ -> Sub.none
    , view = view
    }
