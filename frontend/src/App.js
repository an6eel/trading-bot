import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import {StocksView} from './components/views/stocks/StocksView'
import {StockDetailsView} from './components/views/stockDetails/StockDetailsView'

export const App = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/">
                    <Redirect to="/stocks" />
                </Route>
                <Route path="/stocks">
                    <StocksView/>
                </Route>
                <Route path="/stockdetails">
                    <StockDetailsView/>
                </Route>
            </Switch>
        </Router>
    )
}


export default App;
